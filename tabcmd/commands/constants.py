
class Constants:
    login_error = "401001"
    invalid_credentials = "401002"
    source_already_exists = "409006"
    source_not_found = "404005"
    forbidden = "403022"
    user_already_member_of_site = "409017"


class Errors:

    def is_expired_session(error):
        return error.code == Constants.invalid_credentials

    def check_common_error_codes(logger, error):
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
        if error.code.startswith("404"):
            logger.error("{0} Not Found: Resource cannot be located".format(error.code))
        elif error.code.startswith("405"):
            logger.error("{0} Method not Allowed".format(error.code))
        else:
            logger.error("{0} Error: Server error occurred".format(error.code), error.code)
