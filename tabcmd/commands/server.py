import os
import sys
from tabcmd.commands.constants import Errors
import tableauserverclient as TSC


class Server:
    # syntactic sugar for specific content types
    @staticmethod
    def get_workbook_item(logger, server, workbook_name):
        return Server.get_items_by_name(logger, server.workbooks, workbook_name)[0]

    @staticmethod
    def get_workbook_id(logger, server, workbook_name):
        return Server.get_workbook_item(logger, server, workbook_name).id

    @staticmethod
    def get_data_source_item(logger, server, data_source_name):
        return Server.get_items_by_name(logger, server.datasources, data_source_name)[0]

    @staticmethod
    def get_data_source_id(logger, server, data_source_name):
        return Server.get_data_source_item(logger, server, data_source_name).id

    @staticmethod
    def find_group(logger, server, group_name):
        return Server.get_items_by_name(logger, server.groups, group_name)[0]

    @staticmethod
    def find_group_id(logger, server, group_name):
        return Server.get_items_by_name(logger, server.groups, group_name)[0].id

    @staticmethod
    def find_user_id(logger, server, username):
        return Server.get_items_by_name(logger, server.users, username)[0].id

    @staticmethod
    def get_items_by_name(logger, item_endpoint, item_name):
        logger.debug("get `{0}` from {1}".format(item_name, item_endpoint))
        req_option = TSC.RequestOptions()
        req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, item_name))
        all_items, pagination_item = item_endpoint.get(req_option)
        if all_items is None or all_items == []:
            raise TSC.ServerResponseError(
                "404", "No items returned for name", "Fetching {0} from {1}".format(item_name, item_endpoint)
            )
        if len(all_items) > 1:
            logger.debug("multiple items of this name were found. Returning first page.")
        return all_items

    # Actual server requests
    @staticmethod
    def get_sites(server):
        sites, pagination = server.sites.get()
        return sites

    @staticmethod
    def get_site_for_command(logger, server, args, session):
        if args.site_name:
            site_item = Server.get_items_by_name(logger, server.sites, args.site_name)[0]
        else:
            site_item = server.sites.get_by_id(session.site_id)
        if not site_item:
            Server.exit_with_error(logger, "Could not get site info from server")
        return site_item

    @staticmethod
    def exit_with_error(logger, message, exception=None):
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
                Errors.check_common_error_codes(logger.error, exception)
        except Exception as exc:
            print("Error during log call from exception - {}".format(exc.__class__ or message))
        sys.exit(1)

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

    @staticmethod
    def get_project_by_name_and_parent_path(logger, server, project_name, parent_path):
        logger.debug("Project by name and path: {0}, {1}".format(project_name, parent_path))
        project_tree = Server._parse_project_path_to_list(parent_path)
        if not project_name:
            project = Server._get_parent_project_from_tree(logger, server, project_tree)
        else:
            parent = Server._get_parent_project_from_tree(logger, server, project_tree)
            project = Server._get_project_by_name_and_parent(logger, server, project_name, parent)
        if not project:
            raise TSC.server.ServerResponseError(
                "404", "Could not find project {0}/{1}".format(parent_path, project_name)
            )
        return project

    @staticmethod
    def _parse_project_path_to_list(project_path):
        if project_path is None:
            return []
        return project_path.split("/")

    @staticmethod
    def _get_project_by_name_and_parent(logger, server, project_name, parent):
        logger.debug("get by name and parent: {0}, {1}".format(project_name, parent))
        # get by name to narrow down the list
        projects = Server.get_items_by_name(logger, server.projects, project_name)
        if parent is not None:
            parent_id = parent.id
            for project in projects:
                if project.parent_id == parent_id:
                    return project
        return projects[0]

    @staticmethod
    def _get_parent_project_from_tree(logger, server, hierarchy):
        logger.debug("get parent project from tree: {0}".format(hierarchy))
        tree_height = len(hierarchy)
        if tree_height == 0:
            return None
        elif tree_height == 1:
            return Server._get_project_by_name_and_parent(logger, server, hierarchy[0], None)
        else:
            name = hierarchy.pop(tree_height - 1)
            return Server._get_project_by_name_and_parent(
                logger, server, name, Server._get_parent_project_from_tree(logger, server, hierarchy)
            )
