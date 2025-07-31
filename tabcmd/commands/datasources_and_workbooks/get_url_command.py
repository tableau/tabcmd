import inspect

import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks
from .datasources_workbooks_views_url_parser import DatasourcesWorkbooksAndViewsUrlParser


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
        file_type = DatasourcesWorkbooksAndViewsUrlParser.get_file_type_from_filename(logger, url, args.filename)

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
        Errors.exit_with_error(logger, message=_("bad_request.detail.invalid_content_type").format(url))

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
            (
                get_url_item,
                server_content_type,
            ) = DatasourcesWorkbooksAndViewsUrlParser.get_url_item_and_item_type_from_view_url(logger, url, server)

            if file_type == "pdf":
                return GetUrl.generate_pdf(logger, server_content_type, args, get_url_item)
            elif file_type == "png":
                return GetUrl.generate_png(logger, server_content_type, args, get_url_item)
            elif file_type == "csv":
                return GetUrl.generate_csv(logger, server_content_type, args, get_url_item)
        # all the known options above will return early. If we get here we are confused.
        Errors.exit_with_error(logger, message=_("get.extension.not_found"))

    @staticmethod
    def generate_pdf(logger, server_content_type, args, get_url_item):
        logger.trace("Entered method " + inspect.stack()[0].function)
        try:
            logger.debug(_("content_type.view") + ": {}".format(get_url_item.name))
            req_option_pdf = TSC.PDFRequestOptions(maxage=1)
            DatasourcesAndWorkbooks.apply_values_from_url_params(logger, req_option_pdf, args.url)
            server_content_type.populate_pdf(get_url_item, req_option_pdf)
            filename = GetUrl.filename_from_args(args.filename, get_url_item.name, "pdf")
            DatasourcesAndWorkbooks.save_to_file(logger, get_url_item.pdf, filename)
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def generate_png(logger, server_content_type, args, get_url_item):
        logger.trace("Entered method " + inspect.stack()[0].function)
        try:
            logger.debug(_("content_type.view") + ": {}".format(get_url_item.name))
            req_option_png = TSC.ImageRequestOptions(maxage=1)
            DatasourcesAndWorkbooks.apply_values_from_url_params(logger, req_option_png, args.url)
            server_content_type.populate_image(get_url_item, req_option_png)
            filename = GetUrl.filename_from_args(args.filename, get_url_item.name, "png")
            DatasourcesAndWorkbooks.save_to_file(logger, get_url_item.image, filename)
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def generate_csv(logger, server_content_type, args, get_url_item):
        logger.trace("Entered method " + inspect.stack()[0].function)
        try:
            logger.debug(_("content_type.view") + ": {}".format(get_url_item.name))
            req_option_csv = TSC.CSVRequestOptions(maxage=1)
            DatasourcesAndWorkbooks.apply_values_from_url_params(logger, req_option_csv, args.url)
            server_content_type.populate_csv(get_url_item, req_option_csv)
            file_name_with_path = GetUrl.filename_from_args(args.filename, get_url_item.name, "csv")
            DatasourcesAndWorkbooks.save_to_data_file(logger, get_url_item.csv, file_name_with_path)
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def generate_twb(logger, server, args, file_extension, url):
        logger.trace("Entered method " + inspect.stack()[0].function)
        workbook_name = DatasourcesWorkbooksAndViewsUrlParser.get_resource_name(url, logger)
        try:
            target_workbook = GetUrl.get_wb_by_content_url(logger, server, workbook_name)
            logger.debug(_("content_type.workbook") + ": {}".format(workbook_name))
            file_name_with_path = GetUrl.filename_from_args(args.filename, workbook_name, file_extension)
            # the download method will add an extension. How do I tell which one?
            file_name_with_path = DatasourcesWorkbooksAndViewsUrlParser.get_name_without_possible_extension(
                file_name_with_path
            )
            file_name_with_ext = "{}.{}".format(file_name_with_path, file_extension)
            logger.debug("Saving as {}".format(file_name_with_ext))
            server.workbooks.download(target_workbook.id, filepath=file_name_with_path, include_extract=True)
            logger.info(_("export.success").format(target_workbook.name, file_name_with_ext))
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

    @staticmethod
    def generate_tds(logger, server, args, file_extension):
        logger.trace("Entered method " + inspect.stack()[0].function)
        datasource_name = DatasourcesWorkbooksAndViewsUrlParser.get_resource_name(args.url, logger)
        try:
            target_datasource = GetUrl.get_ds_by_content_url(logger, server, datasource_name)
            logger.debug(_("content_type.datasource") + ": {}".format(datasource_name))
            file_name_with_path = GetUrl.filename_from_args(args.filename, datasource_name, file_extension)
            # the download method will add an extension
            file_name_with_path = DatasourcesWorkbooksAndViewsUrlParser.get_name_without_possible_extension(
                file_name_with_path
            )
            file_name_with_ext = "{}.{}".format(file_name_with_path, file_extension)
            logger.debug("Saving as {}".format(file_name_with_ext))
            server.datasources.download(target_datasource.id, filepath=file_name_with_path, include_extract=True)
            logger.info(_("export.success").format(target_datasource.name, file_name_with_ext))
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)
