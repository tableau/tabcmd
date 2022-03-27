import os
import sys
import tableauserverclient as TSC


class Commands:
    def __init__(self, args):
        self.logger = None
        self.username = args.username
        self.password = args.password
        self.server = args.server
        self.site = args.site
        self.token_name = args.token_name
        self.personal_token = args.token
        self.logging_level = args.logging_level

    @staticmethod
    def get_workbook_item(server, workbook_name):
        return Commands.get_items_by_name(server.workbooks, workbook_name)[0]

    @staticmethod
    def get_workbook_id(server, workbook_name):
        return Commands.get_workbook_item(server, workbook_name).id

    @staticmethod
    def get_data_source_item(server, data_source_name):
        return Commands.get_items_by_name(server.datasources, data_source_name)[0]

    @staticmethod
    def get_data_source_id(server, data_source_name):
        return Commands.get_data_source_item(server, data_source_name).id

    @staticmethod
    def get_items_by_name(item_endpoint, item_name):
        # print("get `{0}` from {1}".format(item_name, item_endpoint))
        req_option = TSC.RequestOptions()
        req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, item_name))
        all_items, pagination_item = item_endpoint.get(req_option)
        if all_items is None or all_items == []:
            raise TSC.ServerResponseError(
                "404", "No items returned for name", "Fetching {0} from {1}".format(item_name, item_endpoint)
            )
        # if len(all_items) > 1:
        #     print("multiple items of this name were found. Returning first page.")
        return all_items

    @staticmethod
    def get_site_for_command(logger, server, args, session):
        if args.site_name:
            site_item = server.sites.get_by_name(args.site_name)
        else:
            site_item = server.sites.get_by_id(session.site_id)
        if not site_item:
            Commands.exit_with_error(logger, "Could not get site info from server")
        return site_item

    @staticmethod
    def exit_with_error(logger, message, exception=None):
        try:
            if message and not exception:
                logger.error(message)
            if exception:
                if Commands.is_expired_session_error(exception):
                    logger.info("Your session has expired. Signing out to clear session...")
                    # TODO: add session as an argument to this method
                    #  and add the full command line as a field in Session?
                    # session.renew_session()
                    return
                if message:
                    logger.debug(message)
                Commands.check_common_error_codes(logger, exception)
        except Exception as exc:
            print("Error during log call from exception - {} {}".format(exc.__class__, message))
        sys.exit(1)

    @staticmethod
    def is_expired_session_error(error):
        return error.code == "401002"

    @staticmethod
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

    @staticmethod
    def get_filename_extension_if_tableau_type(logger, filename):
        logger.debug("Filename given: {}".format(filename))
        source_file, source_type = os.path.splitext(filename)  # returns .ext
        source_type = source_type.lstrip(".")
        logger.debug("Parsed into {0}, {1}".format(source_file, source_type))
        if not source_type:
            raise ValueError("Filename `{}` must have a file extension.".format(filename))
        possible_types = ["twbx", "twb", "tdsx", "tds", "hyper"]
        if source_type in possible_types:
            return source_type
        raise ValueError(
            "Filename `{0}` does not have an appropriate file extension: found `{1}`.".format(filename, source_type)
        )
