import os

from uuid import UUID

from tabcmd.commands.constants import Errors
from tabcmd.commands.datasources_and_workbooks.datasources_and_workbooks_command import DatasourcesAndWorkbooks
from tabcmd.commands.server import Server
from tabcmd.execution.localize import _


class DatasourcesWorkbooksAndViewsUrlParser(Server):
    """
    Base Class for parsing & fetching Datasources, Workbooks, Views & Custom Views information from get/export URLs
    """

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def get_view_url_from_names(wb_name, view_name):
        return "{}/sheets/{}".format(wb_name, view_name)

    @staticmethod
    def parse_export_url_to_workbook_view_and_custom_view(logger, url):
        # input should be workbook_name/view_name or /workbook_name/view_name
        # or workbook_name/view_name/custom_view_id/custom_view_name
        name_parts = DatasourcesWorkbooksAndViewsUrlParser.validate_and_extract_url_parts(logger, url)
        if len(name_parts) == 2:
            workbook = name_parts[0]
            view = DatasourcesWorkbooksAndViewsUrlParser.get_view_url_from_names(workbook, name_parts[1])
            return view, workbook, None, None
        elif len(name_parts) == 4:
            workbook = name_parts[0]
            view = DatasourcesWorkbooksAndViewsUrlParser.get_view_url_from_names(workbook, name_parts[1])
            custom_view_id = name_parts[2]
            DatasourcesWorkbooksAndViewsUrlParser.verify_valid_custom_view_id(logger, custom_view_id)
            custom_view_name = name_parts[3]
            return view, workbook, custom_view_id, custom_view_name
        else:
            return None, None, None, None

    @staticmethod
    def validate_and_extract_url_parts(logger, url):
        logger.info(_("export.status").format(url))
        if " " in url:
            Errors.exit_with_error(logger, _("export.errors.white_space_workbook_view"))
        if "?" in url:
            url = url.split("?")[0]
        url = url.lstrip("/")  # strip opening / if present
        return url.split("/")

    @staticmethod
    def get_export_item_and_server_content_type_from_export_url(view_content_url, logger, server, custom_view_id):
        return DatasourcesWorkbooksAndViewsUrlParser.get_content_and_server_content_type_from_url(
            logger, server, view_content_url, custom_view_id
        )

    ################### GetURL Methods ##############################

    @staticmethod
    def explain_expected_get_url(logger, url: str, command: str):
        view_example = "/views/<workbookname>/<viewname>[.ext]"
        custom_view_example = "/views/<workbookname>/<viewname>/<customviewid>/<customviewname>[.ext]"
        wb_example = "/workbooks/<workbookname>[.ext]"
        ds_example = "/datasources/<datasourcename[.ext]"
        message = _("export.errors.requires_workbook_view_param").format(
            command
        ) + "Given: {0}. Accepted values: {1}, {2}, {3}, {4}".format(
            url, view_example, custom_view_example, wb_example, ds_example
        )
        Errors.exit_with_error(logger, message)

    @staticmethod
    def get_file_type_from_filename(logger, url, file_name):
        logger.debug("Choosing between {}, {}".format(file_name, url))
        file_name = file_name or url
        logger.debug(_("get.options.file") + ": {}".format(file_name))  # Name to save the file as
        type_of_file = DatasourcesWorkbooksAndViewsUrlParser.get_file_extension(file_name)

        if not type_of_file and file_name is not None:
            # check the url
            backup = DatasourcesWorkbooksAndViewsUrlParser.get_file_extension(url)
            if backup is not None:
                type_of_file = backup
            else:
                Errors.exit_with_error(logger, _("get.extension.not_found").format(file_name))

        logger.debug("filetype: {}".format(type_of_file))
        if type_of_file in ["pdf", "csv", "png", "twb", "twbx", "tdsx", "tds"]:
            return type_of_file

        Errors.exit_with_error(logger, _("get.extension.not_found").format(file_name))

    @staticmethod
    def get_file_extension(path):
        path_segments = os.path.split(path)
        filename = path_segments[-1]
        filename_segments = filename.split(".")
        extension = filename_segments[-1]
        extension = DatasourcesWorkbooksAndViewsUrlParser.strip_query_params(extension)
        return extension

    @staticmethod
    def strip_query_params(filename):
        if "?" in filename:
            return filename.split("?")[0]
        else:
            return filename

    @staticmethod
    def get_name_without_possible_extension(filename):
        return filename.split(".")[0]

    @staticmethod
    def get_resource_name(url: str, logger):  # workbooks/wb-name" -> "wb-name", datasource/ds-name -> ds-name
        url = url.lstrip("/")  # strip opening / if present
        name_parts = url.split("/")
        if len(name_parts) != 2:
            DatasourcesWorkbooksAndViewsUrlParser.explain_expected_get_url(logger, url, "GetUrl")
        resource_name_with_params = name_parts[::-1][0]  # last part
        resource_name_with_ext = DatasourcesWorkbooksAndViewsUrlParser.strip_query_params(resource_name_with_params)
        resource_name = DatasourcesWorkbooksAndViewsUrlParser.get_name_without_possible_extension(
            resource_name_with_ext
        )
        return resource_name

    @staticmethod
    def get_view_url_from_get_url(logger, url):  # "views/wb-name/view-name" -> wb-name/sheets/view-name
        name_parts = url.split("/")  # ['views', 'wb-name', 'view-name']
        if len(name_parts) != 3:
            DatasourcesWorkbooksAndViewsUrlParser.explain_expected_get_url(logger, url, "GetUrl")
        workbook_name = name_parts[1]
        view_name = name_parts[::-1][0]
        view_name = DatasourcesWorkbooksAndViewsUrlParser.strip_query_params(view_name)
        view_name = DatasourcesWorkbooksAndViewsUrlParser.get_name_without_possible_extension(view_name)
        return DatasourcesWorkbooksAndViewsUrlParser.get_view_url_from_names(workbook_name, view_name)

    @staticmethod
    def get_custom_view_parts_from_get_url(logger, url):
        name_parts = url.split("/")  # ['views', 'wb-name', 'view-name', 'custom-view-id', 'custom-view-name']
        if len(name_parts) != 5:
            DatasourcesWorkbooksAndViewsUrlParser.explain_expected_get_url(logger, url, "GetUrl")
        workbook_name = name_parts[1]
        view_name = name_parts[2]
        custom_view_id = name_parts[3]
        DatasourcesWorkbooksAndViewsUrlParser.verify_valid_custom_view_id(logger, custom_view_id)
        custom_view_name = name_parts[::-1][0]
        custom_view_name = DatasourcesWorkbooksAndViewsUrlParser.strip_query_params(custom_view_name)
        custom_view_name = DatasourcesWorkbooksAndViewsUrlParser.get_name_without_possible_extension(custom_view_name)
        return (
            DatasourcesWorkbooksAndViewsUrlParser.get_view_url_from_names(workbook_name, view_name),
            custom_view_id,
            custom_view_name,
        )

    @staticmethod
    def parse_get_view_url_to_view_and_custom_view_parts(logger, url):
        # input should be views/workbook_name/view_name
        # or views/workbook_name/view_name/custom_view_id/custom_view_name
        name_parts = DatasourcesWorkbooksAndViewsUrlParser.validate_and_extract_url_parts(logger, url)
        if len(name_parts) == 3:
            return DatasourcesWorkbooksAndViewsUrlParser.get_view_url_from_get_url(logger, url), None, None
        elif len(name_parts) == 5:
            return DatasourcesWorkbooksAndViewsUrlParser.get_custom_view_parts_from_get_url(logger, url)
        else:
            DatasourcesWorkbooksAndViewsUrlParser.explain_expected_get_url(logger, url, "GetUrl")

    @staticmethod
    def get_url_item_and_item_type_from_view_url(logger, url, server):
        (
            view_url,
            custom_view_id,
            custom_view_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.parse_get_view_url_to_view_and_custom_view_parts(logger, url)

        return DatasourcesWorkbooksAndViewsUrlParser.get_content_and_server_content_type_from_url(
            logger, server, view_url, custom_view_id
        )

    @staticmethod
    def get_content_and_server_content_type_from_url(logger, server, view_content_url, custom_view_id):
        item = DatasourcesAndWorkbooks.get_view_by_content_url(logger, server, view_content_url)
        server_content_type = server.views

        if custom_view_id:
            custom_view_item = DatasourcesAndWorkbooks.get_custom_view_by_id(logger, server, custom_view_id)
            if custom_view_item.view.id != item.id:
                Errors.exit_with_error(logger, "Invalid custom view URL provided")
            server_content_type = server.custom_views
            item = custom_view_item
        return item, server_content_type

    @staticmethod
    def verify_valid_custom_view_id(logger, custom_view_id):
        try:
            UUID(custom_view_id)
        except ValueError:
            Errors.exit_with_error(logger, _("export.errors.requires_valid_custom_view_uuid"))
