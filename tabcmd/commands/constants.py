import inspect
import sys

from tableauserverclient import ServerResponseError

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
            return error.code == Constants.source_already_exists

    @staticmethod
    def is_login_error(error):
        if hasattr(error, "code"):
            return error.code == Constants.login_error

    @staticmethod
    def is_server_response_error(error):
        return isinstance(error, ServerResponseError)

    # https://gist.github.com/FredLoney/5454553
    @staticmethod
    def log_stack(logger):
        try:
            """The log header message formatter."""
            HEADER_FMT = "Printing Call Stack at %s::%s"
            """The log stack message formatter."""
            STACK_FMT = "%s, line %d in function %s."
            stack = inspect.stack()
            here = stack[0]
            file, line, func = here[1:4]
            start = 0
            n_lines = 5
            logger.trace(HEADER_FMT % (file, func))

            for frame in stack[start + 2 : n_lines]:
                file, line, func = frame[1:4]
                logger.trace(STACK_FMT % (file, line, func))
        except Exception as e:
            logger.info("Error printing stack trace:", e)

    @staticmethod
    def exit_with_error(logger, message=None, exception=None):
        try:
            Errors.log_stack(logger)
            if message and not exception:
                logger.error(message)
            if exception:
                if message:
                    logger.debug("Error message: " + message)
                Errors.check_common_error_codes_and_explain(logger, exception)
        except Exception as exc:
            print(sys.stderr, "Error during log call from exception - {}".format(exc))
        try:
            logger.info("Exiting...")
        except Exception:
            print(sys.stderr, "Exiting...")
        sys.exit(1)

    @staticmethod
    def check_common_error_codes_and_explain(logger, exception):
        if Errors.is_server_response_error(exception):
            logger.error(_("publish.errors.unexpected_server_response").format(exception))
            if Errors.is_expired_session(exception):
                logger.error(_("session.errors.session_expired"))
                # TODO: add session as an argument to this method
                #  and add the full command line as a field in Session?
                # "session.session_expired_login"))
                # session.renew_session
                return
            if exception.code == Constants.source_not_found:
                logger.error(_("publish.errors.server_resource_not_found"), exception)
        else:
            logger.error(exception)
