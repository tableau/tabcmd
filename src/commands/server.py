import os
import tableauserverclient as TSC

from src.commands.constants import Errors
from src.execution.localize import _


class Server:
    # syntactic sugar for specific content types
    @staticmethod
    def get_workbook_item(logger, server, workbook_name, container=None):
        try:
            return Server.get_items_by_name(logger, server.workbooks, workbook_name, container=None)[0]
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def get_workbook_id(logger, server, workbook_name, container=None):
        return Server.get_workbook_item(logger, server, workbook_name, container=None).id

    @staticmethod
    def get_data_source_item(logger, server, data_source_name, container=None):
        try:
            return Server.get_items_by_name(logger, server.datasources, data_source_name, container=None)[0]
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def get_data_source_id(logger, server, data_source_name, container=None):
        return Server.get_data_source_item(logger, server, data_source_name, container=None).id

    @staticmethod
    def find_group(logger, server, group_name):
        try:
            return Server.get_items_by_name(logger, server.groups, group_name)[0]
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def find_group_id(logger, server, group_name):
        return Server.find_group(logger, server, group_name)[0].id

    @staticmethod
    def find_user_id(logger, server, username):
        try:
            return Server.get_items_by_name(logger, server.users, username)[0].id
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def get_items_by_name(logger, item_endpoint, item_name, container=None):
        logger.debug(_("export.status").format(item_name))
        req_option = TSC.RequestOptions()
        req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, item_name))
        if container:
            logger.debug("Searching in project {}".format(container))
            req_option.filter.add(
                TSC.Filter(TSC.RequestOptions.Field.ParentProjectId, TSC.RequestOptions.Operator.Equals, container)
            )
        all_items, pagination_item = item_endpoint.get(req_option)
        if all_items is None or all_items == []:
            raise ValueError(_("publish.errors.server_resource_not_found"))
        if len(all_items) > 1:
            logger.debug("{}+ items of this name were found. Returning first page.".format(len(all_items)))
        return all_items

    # Get site by name or get currently logged in site
    @staticmethod
    def get_site_for_command_or_throw(logger, server, args):
        if args.site_name:
            try:
                site_item = Server.get_items_by_name(logger, server.sites, args.site_name)[0]
            except Exception as e:
                Errors.exit_with_error(logger, exception=e)
        else:
            logger.debug("Use logged in site")
            site_item = server.sites.get_by_id(server.site_id)
            if not site_item:
                raise ResourceWarning("Could not get site from server")
        return site_item

    @staticmethod
    def get_filename_extension_if_tableau_type(logger, filename):
        logger.debug("Filename given: {}".format(filename))
        source_file, source_type = os.path.splitext(filename)  # returns .ext
        source_type = source_type.lstrip(".")
        possible_types = ["twbx", "twb", "tdsx", "tds", "hyper"]
        if source_type and source_type in possible_types:
            return source_type
        else:
            raise ValueError(
                "Filename `{0}` does not have an appropriate file extension: found `{1}`.".format(filename, source_type)
            )

    @staticmethod
    def get_project_by_name_and_parent_path(logger, server, project_name, parent_path):
        logger.debug(_("content_type.project") + ":{0}, {1}".format(parent_path, project_name))
        project_tree = Server._parse_project_path_to_list(parent_path)
        if not project_name:
            project = Server._get_parent_project_from_tree(logger, server, project_tree)
        else:
            parent = Server._get_parent_project_from_tree(logger, server, project_tree)
            project = Server._get_project_by_name_and_parent(logger, server, project_name, parent)
        if not project:
            Errors.exit_with_error(logger, message=_("publish.errors.server_resource_not_found"))
        return project

    @staticmethod
    def _parse_project_path_to_list(project_path):
        if project_path is None:
            return []
        return project_path.split("/")

    @staticmethod
    def _get_project_by_name_and_parent(logger, server, project_name, parent):
        # logger.debug("get by name and parent: {0}, {1}".format(project_name, parent))
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
        # logger.debug("get parent project from tree: {0}".format(hierarchy))
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
