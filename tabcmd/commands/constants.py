import sys
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

    @staticmethod
    def exit_with_error(logger, message=None, exception=None):
        try:
            if message and not exception:
                logger.error(message)
            if exception:
                if Errors.is_expired_session(exception):
                    logger.error(_("session.errors.session_expired"))
                    # TODO: add session as an argument to this method
                    #  and add the full command line as a field in Session?
                    # "session.session_expired_login"))
                    # session.renew_session()
                if message:
                    logger.debug(message)
                Errors.check_common_error_codes_and_explain(logger, exception)
        except Exception as exc:
            print("Error during log call from exception - {} {}".format(exc.__class__, message))
        sys.exit(1)

    @staticmethod
    def check_common_error_codes_and_explain(logger, error):
        logger.error(error)
