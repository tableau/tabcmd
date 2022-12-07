import os
from typing import List, Optional

import tableauserverclient as TSC

from tabcmd.commands.constants import Errors
from tabcmd.execution.localize import _


class Server:
    # syntactic sugar for specific content types
    @staticmethod
    def get_workbook_item(logger, server, workbook_name, container=None):
        try:
            return Server.get_items_by_name(logger, server.workbooks, workbook_name, container)[0]
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def get_workbook_id(logger, server, workbook_name, container=None):
        return Server.get_workbook_item(logger, server, workbook_name, container).id

    @staticmethod
    def get_data_source_item(logger, server, data_source_name, container=None):
        try:
            return Server.get_items_by_name(logger, server.datasources, data_source_name, container)[0]
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def get_data_source_id(logger, server, data_source_name, container=None):
        return Server.get_data_source_item(logger, server, data_source_name, container).id

    @staticmethod
    def find_group(logger, server, group_name):
        try:
            return Server.get_items_by_name(logger, server.groups, group_name)[0]
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def find_user(logger, server, username):
        return Server.get_items_by_name(logger, server.users, username)[0]

    @staticmethod
    def get_items_by_name(logger, item_endpoint, item_name: str, container: Optional[TSC.ProjectItem] = None) -> List:
        # TODO: typing should reflect that this returns TSC.TableauItem and item_endpoint is of type TSC.QuerysetEndpoint[same]
        item_log_name: str = "[{0}] {1}".format(type(item_endpoint).__name__, item_name)
        if container:
            container_name: str = "({0}) {1}".format(container.__class__, container.name)
            item_log_name = "{0}/{1}".format(container_name, item_log_name)
        logger.debug(_("export.status").format(item_log_name))
        req_option = TSC.RequestOptions()
        req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, item_name))
        all_items, pagination_item = item_endpoint.get(req_option)
        if all_items is None or all_items == []:
            raise TSC.ServerResponseError(
                code=404,
                summary=_("errors.xmlapi.not_found"),
                detail=_("errors.xmlapi.not_found") + ": " + item_log_name,
            )
        if len(all_items) == 1:
            logger.debug("Exactly one result found")
            result = all_items
        if len(all_items) > 1:
            logger.debug(
                "{}+ items of this name were found: {}".format(
                    len(all_items), all_items[0].name + ", " + all_items[1].name + ", ..."
                )
            )

            if container:
                container_id = container.id
                logger.debug("Filtering to items in project {}".format(container.id))
                result = list(filter(lambda item: item.project_id == container_id, all_items))
            else:
                result = all_items

        return result

    # Get site by name or get currently logged in site
    @staticmethod
    def get_site_for_command_or_throw(logger, server, site_name):
        if site_name:
            site_item = Server.get_site_by_name(logger, server, site_name)
        else:
            logger.debug("Use logged in site")
            site_item = server.sites.get_by_id(server.site_id)
            if not site_item:
                raise ResourceWarning("Could not get site from server")
        return site_item

    @staticmethod
    def get_site_by_name(logger, server, site_name) -> TSC.SiteItem:
        try:
            # sites don't use the normal filter
            site_item = server.sites.get_by_name(site_name)
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)
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
    def get_project_by_name_and_parent_path(logger, server, project_name: str, parent_path: str) -> TSC.ProjectItem:
        logger.debug(_("content_type.project") + ":{0}, {1}".format(parent_path, project_name))
        if not parent_path:
            if not project_name:
                project_name = "Default"
            project: TSC.ProjectItem = Server.get_items_by_name(logger, server.projects, project_name, None)[0]
            return project

        project_tree: List[str] = Server._parse_project_path_to_list(parent_path)
        if not project_name:
            project = Server._get_parent_project_from_tree(logger, server, project_tree)
            return project

        parent = Server._get_parent_project_from_tree(logger, server, project_tree)
        logger.debug(parent)
        project = Server._get_project_by_name_and_parent(logger, server, project_name, parent)
        logger.debug(project)
        if not project:
            Errors.exit_with_error(logger, message=_("publish.errors.server_resource_not_found"))
        return project

    @staticmethod
    def _parse_project_path_to_list(project_path: str):
        if project_path is None or project_path == "":
            return []
        if project_path.find("/") == -1:
            return [project_path]
        return project_path.split("/")

    @staticmethod
    def _get_project_by_name_and_parent(logger, server, project_name: str, parent: Optional[TSC.ProjectItem]):
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
    def _get_parent_project_from_tree(logger, server, hierarchy: List[str]):
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
