import sys


class Constants:
    login_error = "401001"
    invalid_credentials = "401002"
    source_already_exists = "409006"
    source_not_found = "404005"
    forbidden = "403022"
    user_already_member_of_site = "409017"


class Errors:
    @staticmethod
    def exit_with_error(logger, message, exception=None):
        logger.debug("exit with error")
        try:
            if message and not exception:
                logger.error(message)
            if exception:
                if Errors.is_expired_session(exception):
                    logger.info("Your session has expired. Signing out to clear session...")
                    # TODO: add session as an argument to this method
                    #  and add the full command line as a field in Session?
                    # session.renew_session()
                    return
                if message:
                    logger.debug(message)
                Errors.check_common_error_codes_and_explain(logger, exception)
        except Exception as exc:
            print("Error during log call from exception - {} {}".format(exc.__class__, message))
        sys.exit(1)

    @staticmethod
    def is_expired_session(error):
        return error.code == Constants.invalid_credentials

    # pass in a logger at defined level, so we can call this important or not
    @staticmethod
    def check_common_error_codes_and_explain(logger, error):
        logger.debug(error)
        if error.code.startswith("400"):
            logger.error(
                "{0} Bad request: Tableau Server cannot parse or interpret the message in the request".format(
                    error.code
                )
            )
        elif error.code.startswith("401"):
            logger.error("{0} User not Authenticated".format(error.code))
        elif error.code.startswith("403"):
            logger.error("{0} Forbidden: Request was not authorized".format(error.code))
        elif error.code.startswith("404"):
            logger.error("{0} Not Found: Resource cannot be located".format(error.code))
        elif error.code.startswith("405"):
            logger.error("{0} Method not Allowed".format(error.code))
        else:
            logger.error("{0} Error: Server error occurred".format(error.code))
