import inspect
import sys
from typing import Optional

import tableauserverclient

from tabcmd.execution.localize import _


class Constants:
    login_error = "401001"
    invalid_credentials = "401002"
    source_not_found = "404005"
    forbidden = "403022"
    resource_conflict_general = "409"
    source_already_exists = "409006"
    user_already_member_of_site = "409017"


class Errors:
    @staticmethod
    def is_expired_session(error):
        if hasattr(error, "code"):
            return error.code == Constants.invalid_credentials

    @staticmethod
    def is_resource_conflict(error):
        if hasattr(error, "code"):
            return error.code.startswith(Constants.resource_conflict_general)

    @staticmethod
    def is_login_error(error):
        if hasattr(error, "code"):
            return error.code == Constants.login_error

    # https://gist.github.com/FredLoney/5454553
    @staticmethod
    def log_stack(logger):
        if not logger:
            print("logger not available: cannot show stack")
            return
        try:
            """The log header message formatter."""
            HEADER_FMT = "Printing Call Stack at %s::%s"
            """The log stack message formatter."""
            STACK_FMT = "%s, line %d in function %s."
            stack = inspect.stack()
            here = stack[0]
            file, line, func = here[1:4]
            start = 1
            n_lines = 5
            logger.debug(HEADER_FMT % (file, func))
            for frame in stack[start + 1 : n_lines]:
                file, line, func = frame[1:4]
                logger.debug(STACK_FMT % (file, line, func))
        except Exception as e:
            logger.info("Error printing stack trace:", e)

    @staticmethod
    def exit_with_error(logger, message: Optional[str] = None, exception: Optional[Exception] = None):
        suggest_logs_message = "Exiting with error...\nSee logs for more information."
        try:
            if message and not exception:
                logger.error(message)
                Errors.log_stack(logger)
            elif exception:
                if message:
                    logger.info("\nError message: " + message)
                Errors.check_common_error_codes_and_explain(logger, exception)
            else:
                logger.info("No exception or message provided")

        except Exception as exc:
            print("Error during log call from exception - {} {}".format(exc.__class__, message))

        print("")
        print(suggest_logs_message)
        sys.exit(1)

    @staticmethod
    def check_common_error_codes_and_explain(logger, exception: Exception):
        # most errors contain as much info in the message as we can get from the code
        # identify any that we can add useful detail for and include them here
        if Errors.is_expired_session(exception):
            # catch this one so we can attempt to refresh the session before telling them it failed
            logger.error(_("session.errors.session_expired"))
            # TODO: add session as an argument to this method
            #  and add the full command line as a field in Session?
            # "session.session_expired_login"))
            # session.renew_session()
            return
        if exception.__class__ == tableauserverclient.ServerResponseError:
            logger.debug("Server response error")

            logger.error(exception)
        else:
            # logger.exception prints a really long ugly stack, generally not useful to users. 
            # Should print that to the log, but not console.
            logger.error(exception)
