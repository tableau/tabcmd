import inspect

import tableauserverclient as TSC
from tableauserverclient import ServerResponseError

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class GetUrl(DatasourcesAndWorkbooks):
    """
    This command gets the resource from Tableau Server that's represented
    by the specified (partial) URL. The result is returned as a file.
    """

    name: str = "get"
    description: str = _("get.short_description")
    valid_file_types = {"workbook": ["twbx", "twb"], "datasource": ["tdsx", "tds"], "view": ["pdf", "png", "csv"]}
    valid_content_types = ["workbook", "view", "datasource"]

    @staticmethod
    def define_args(get_url_parser):
        group = get_url_parser.add_argument_group(title=GetUrl.name)
        group.add_argument("url", help=_("refreshextracts.options.url"))
        set_filename_arg(group)
        # these don't need arguments, although that would be a good future addition
        # tabcmd get "/views/Finance/InvestmentGrowth.png?:size=640,480" -f growth.png
        # tabcmd get "/views/Finance/InvestmentGrowth.png?:refresh=yes" -f growth.png

    @staticmethod
    def run_command(args):
        # A view can be returned in PDF, PNG, or CSV (summary data only) format.
        # A Tableau workbook is returned as a TWB if it connects to a datasource/live connection,
        # or a TWBX if it uses an extract.
        # A Tableau datasource is returned as a TDS if it connects to a live connection,
        # or a TDSX if it uses an extract.
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)
        if " " in args.url:
            Errors.exit_with_error(logger, _("export.errors.white_space_workbook_view"))

        url = args.url.lstrip("/")  # strip opening / if present
        content_type = GetUrl.evaluate_content_type(logger, url)
        file_type = GetUrl.get_file_type_from_filename(logger, url, args.filename)

        GetUrl.get_content_as_file(file_type, content_type, logger, args, server, url)

    ## this first set of methods is all parsing the url and file input from the user

    @staticmethod
    def evaluate_content_type(logger, url):
        # specify a view to get using "/views/<workbookname>/<viewname>.<extension>"
        # specify a workbook to get using "/workbooks/<workbookname>.<extension>".
        # specify a datasource to get using "/datasources/<datasourcename>.<extension>"
        content_type = ""
        for content_type in GetUrl.valid_content_types:
            if url.find(content_type) == 0:
                return content_type
        Errors.exit_with_error(logger, message=_("get.errors.invalid_content_type").format(url))

    @staticmethod
    def explain_expected_url(logger, url: str, command: str):
        view_example = "/views/<workbookname>/<viewname>[.ext]"
        wb_example = "/workbooks/<workbookname>[.ext]"
        ds_example = "/datasources/<datasourcename[.ext]"
        # todo when strings are updated # message:str = _("export.errors.requires_resource_param").format(
        message = (
            "The ''{0}'' command requires a resource path in a specific format."
            "Given: {1}. Accepted values: {2}, {3}, {4}".format(command, url, view_example, wb_example, ds_example)
        )
        Errors.exit_with_error(logger, message)

    @staticmethod
    def get_file_type_from_filename(logger, url, file_name):
        logger.debug("Choosing between {}, {}".format(file_name, url))
        file_name = file_name or url
        logger.debug(_("get.options.file") + ": {}".format(file_name))
        type_of_file = GetUrl.get_file_extension(file_name)

        if not type_of_file and file_name is not None:
            # check the url
            backup = GetUrl.get_file_extension(url)
            if backup is not None:
                type_of_file = backup
            else:
                Errors.exit_with_error(logger, _("tabcmd.get.extension.not_found").format(file_name))

        logger.debug("filetype: {}".format(type_of_file))
        if type_of_file in ["pdf", "csv", "png", "twb", "twbx", "tdsx"]:
            return type_of_file

        Errors.exit_with_error(logger, _("tabcmd.get.extension.not_found").format(file_name))

    @staticmethod
    def get_file_extension(filename):
        parts = filename.split(".")
        if len(parts) < 2:
            return None
        extension = parts[1]
        extension = GetUrl.strip_query_params(extension)
        return extension

    @staticmethod
    def strip_query_params(filename):
        if filename.find("?") > 0:
            filename = filename.split("?")[0]
        return filename

    @staticmethod
    def get_name_without_possible_extension(filename):
        if filename.find(".") > 0:
            filename = filename.split(".")[0]
        return filename

    @staticmethod
    def get_resource_name(url: str, logger):  # workbooks/wb-name" -> "wb-name", datasource/ds-name -> ds-name
        url = url.lstrip("/")  # strip opening / if present
        name_parts = url.split("/")
        if len(name_parts) != 2:
            GetUrl.explain_expected_url(logger, url, "GetUrl")
        resource_name_with_params = name_parts[::-1][0]  # last part
        resource_name_with_ext = GetUrl.strip_query_params(resource_name_with_params)
        resource_name = GetUrl.get_name_without_possible_extension(resource_name_with_ext)
        return resource_name

    @staticmethod
    def get_view_url(url, logger):  # "views/wb-name/view-name" -> wb-name/sheets/view-name
        name_parts = url.split("/")  # ['views', 'wb-name', 'view-name']
        if len(name_parts) != 3:
            GetUrl.explain_expected_url(logger, url, "GetUrl")
        workbook_name = name_parts[1]
        view_name = name_parts[::-1][0]
        view_name = GetUrl.strip_query_params(view_name)
        view_name = GetUrl.get_name_without_possible_extension(view_name)
        return DatasourcesAndWorkbooks.get_view_url_from_names(workbook_name, view_name)

    @staticmethod
    def filename_from_args(file_argument, item_name, filetype):
        if file_argument is None:
            file_argument = item_name
        if not file_argument.endswith(filetype):
            file_argument = "{}.{}".format(file_argument, filetype)
        return file_argument

    ## methods below here have done all the parsing and just have to do the download and saving
    ## these should be able to be shared with export

    @staticmethod
    def get_content_as_file(file_type, content_type, logger, args, server, url):
        logger.debug("fetching {} as {}".format(content_type, file_type))
        if content_type == "workbook":
            return GetUrl.generate_twb(logger, server, args, file_type, url)
        elif content_type == "datasource":
            return GetUrl.generate_tds(logger, server, args, file_type)
        elif content_type == "view":
            view_url = GetUrl.get_view_url(url, logger)
            if file_type == "pdf":
                return GetUrl.generate_pdf(logger, server, args, view_url)
            elif file_type == "png":
                return GetUrl.generate_png(logger, server, args, view_url)
            elif file_type == "csv":
                return GetUrl.generate_csv(logger, server, args, view_url)
        # all the known options above will return early. If we get here we are confused.
        Errors.exit_with_error(logger, message=_("tabcmd.get.extension.not_found"))

    @staticmethod
    def generate_pdf(logger, server, args, view_url):
        logger.trace("Entered method " + inspect.stack()[0].function)
        try:
            view_item: TSC.ViewItem = GetUrl.get_view_by_content_url(logger, server, view_url)
            logger.debug(_("content_type.view") + ": {}".format(view_item.name))
            req_option_pdf = TSC.PDFRequestOptions(maxage=1)
            DatasourcesAndWorkbooks.apply_values_from_url_params(logger, req_option_pdf, args.url)
            server.views.populate_pdf(view_item, req_option_pdf)
            filename = GetUrl.filename_from_args(args.filename, view_item.name, "pdf")
            DatasourcesAndWorkbooks.save_to_file(logger, view_item.pdf, filename)
        except Exception as e:
            Errors.exit_with_error(logger, e)

    @staticmethod
    def generate_png(logger, server, args, view_url):
        logger.trace("Entered method " + inspect.stack()[0].function)
        try:
            view_item: TSC.ViewItem = GetUrl.get_view_by_content_url(logger, server, view_url)
            logger.debug(_("content_type.view") + ": {}".format(view_item.name))
            req_option_csv = TSC.ImageRequestOptions(maxage=1)
            DatasourcesAndWorkbooks.apply_values_from_url_params(logger, req_option_csv, args.url)
            server.views.populate_image(view_item, req_option_csv)
            filename = GetUrl.filename_from_args(args.filename, view_item.name, "png")
            DatasourcesAndWorkbooks.save_to_file(logger, view_item.image, filename)
        except Exception as e:
            Errors.exit_with_error(logger, e)

    @staticmethod
    def generate_csv(logger, server, args, view_url):
        logger.trace("Entered method " + inspect.stack()[0].function)
        try:
            view_item: TSC.ViewItem = GetUrl.get_view_by_content_url(logger, server, view_url)
            logger.debug(_("content_type.view") + ": {}".format(view_item.name))
            req_option_csv = TSC.CSVRequestOptions(maxage=1)
            DatasourcesAndWorkbooks.apply_values_from_url_params(logger, req_option_csv, args.url)
            server.views.populate_csv(view_item, req_option_csv)
            file_name_with_path = GetUrl.filename_from_args(args.filename, view_item.name, "csv")
            DatasourcesAndWorkbooks.save_to_data_file(logger, view_item.csv, file_name_with_path)
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def generate_twb(logger, server, args, file_extension, url):
        logger.trace("Entered method " + inspect.stack()[0].function)
        workbook_name = GetUrl.get_resource_name(url, logger)
        try:
            target_workbook = GetUrl.get_wb_by_content_url(logger, server, workbook_name)
            logger.debug(_("content_type.workbook") + ": {}".format(workbook_name))
            file_name_with_path = GetUrl.filename_from_args(args.filename, workbook_name, file_extension)
            # the download method will add an extension. How do I tell which one?
            file_name_with_path = GetUrl.get_name_without_possible_extension(file_name_with_path)
            file_name_with_ext = "{}.{}".format(file_name_with_path, file_extension)
            logger.debug("Saving as {}".format(file_name_with_ext))
            server.workbooks.download(target_workbook.id, filepath=file_name_with_path, no_extract=False)
            logger.info(_("export.success").format(target_workbook.name, file_name_with_ext))
        except Exception as e:
            Errors.exit_with_error(logger, e)

    @staticmethod
    def generate_tds(logger, server, args, file_extension):
        logger.trace("Entered method " + inspect.stack()[0].function)
        datasource_name = GetUrl.get_resource_name(args.url, logger)
        try:
            target_datasource = GetUrl.get_ds_by_content_url(logger, server, datasource_name)
            logger.debug(_("content_type.datasource") + ": {}".format(datasource_name))
            file_name_with_path = GetUrl.filename_from_args(args.filename, datasource_name, file_extension)
            # the download method will add an extension
            file_name_with_path = GetUrl.get_name_without_possible_extension(file_name_with_path)
            file_name_with_ext = "{}.{}".format(file_name_with_path, file_extension)
            logger.debug("Saving as {}".format(file_name_with_ext))
            server.datasources.download(target_datasource.id, filepath=file_name_with_path, no_extract=False)
            logger.info(_("export.success").format(target_datasource.name, file_name_with_ext))
        except Exception as e:
            Errors.exit_with_error(logger, e)
