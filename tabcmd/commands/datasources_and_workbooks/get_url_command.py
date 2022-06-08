import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks
from tabcmd.execution.global_options import *
from tabcmd.commands.constants import Errors
from tabcmd.execution.localize import _

class GetUrl(DatasourcesAndWorkbooks):
    """
    This command gets the resource from Tableau Server that's represented
    by the specified (partial) URL. The result is returned as a file.
    """

    name: str = "get"
    description: str = _("get.short_description")

    @staticmethod
    def define_args(get_url_parser):
        get_url_parser.add_argument(
            "url",
            help=_("createextracts.options.url"),
        )
        set_filename_arg(get_url_parser)
        # to send to the server these are both just set on the url?
        # these don't need arguments, although that would be a good future addition
        # tabcmd get "/views/Finance/InvestmentGrowth.png?:size=640,480" -f growth.png
        # tabcmd get "/views/Finance/InvestmentGrowth.png?:refresh=yes" -f growth.png

    @staticmethod
    def run_command(args):
        # A view can be returned in PDF, PNG, or CSV (summary data only) format.
        # A Tableau workbook is returned as a TWB if it connects to a datasource/live connection,
        # or a TWBX if it uses an extract.
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        file_type = GetUrl.get_download_type(logger, args.filename, args.url)
        logger.debug("Getting file type " + file_type)
        if file_type in ["pdf", "png", "csv"]:
            GetUrl.download_and_save_view(logger, server, args, file_type)
        elif file_type == "twbx" or file_type == "twb":
            GetUrl.download_and_save_wb(logger, server, args, file_type)
        else:
            Errors.exit_with_error(logger, _("common.errors.invalid_file_path"))

    @staticmethod
    def get_download_type(logger, file_name, url):
        type_of_file = None
        if file_name is not None:
            split_file_name = file_name.split(".")
            type_of_file = split_file_name[1]
        else:  # file_name is None, grab from url
            split_url_to_get_extension = url.split(".")
            if len(split_url_to_get_extension) > 1:
                type_of_file = split_url_to_get_extension[1]
            else:
                GetUrl.exit_with_error(logger, _("importcsvsummary.error.unexpected_extension"))
        return type_of_file

    @staticmethod
    def get_name_without_possible_extension(filename):
        split_parts = filename.split(".")
        return split_parts[0]

    @staticmethod
    def get_workbook_name(logger, url):  # something like 'workbooks/Regional.twbx'
        url = url.lstrip('//')  # lose leading slash
        separated_list = url.split("/")
        if len(separated_list) < 2:
            message = _("export.errors.requires_workbook_view_param").format(url)
            Errors.exit_with_error(logger, message=message)
        workbook_name = GetUrl.get_name_without_possible_extension(separated_list[1])
        logger.debug("Got workbook name '{}' from url '{}'".format(workbook_name, url))
        return workbook_name

    @staticmethod
    def get_view_url(logger, url):
        url = url.lstrip('//')  # lose leading slash
        separated_list = url.split("/")
        if len(separated_list) < 3:
            message = _("export.errors.requires_workbook_view_param").format(url)
            Errors.exit_with_error(logger, message=message)
        workbook_name = separated_list[1]
        view_name = GetUrl.get_name_without_possible_extension(separated_list[::-1][0])
        view_url = "{}/sheets/{}".format(workbook_name, view_name)
        logger.debug("Got view url '{}' from url '{}'".format(view_url, url))
        return view_url

    @staticmethod
    def get_target_view(args, logger, server):
        try:
            view = GetUrl.get_view_url(logger, args.url)
        except Exception as e:
            GetUrl.exit_with_error(logger, _("errors.xmlapi.invalid_parameter"), e)
        logger.debug("view url: " + view)
        target_view = GetUrl.get_view_by_content_url(logger, server, view)
        return target_view

    @staticmethod
    def set_file_name(item_name, filename, file_format):
        if filename is None:
            file_name_with_path = "{}.{}".format(item_name, file_format)
        else:
            file_name_with_path = filename
        return file_name_with_path

    @staticmethod
    def populate_data(server, target_view, filetype):
        if filetype == "pdf":
            req_option_pdf = TSC.PDFRequestOptions(maxage=1)
            server.views.populate_pdf(target_view, req_option_pdf)
            return target_view.pdf
        elif filetype == "csv":
            req_option_csv = TSC.CSVRequestOptions(maxage=1)
            server.views.populate_csv(target_view, req_option_csv)
            return target_view.csv
        elif filetype == "png":
            req_option_csv = TSC.CSVRequestOptions(maxage=1)
            server.views.populate_csv(target_view, req_option_csv)
            return target_view.png
        else:
            Errors.exit_with_error("Unknown filetype")

    @staticmethod
    def download_and_save_view(logger, server, args, filetype):
        target_view = GetUrl.get_target_view(args, logger, server)
        formatted_file_name = GetUrl.set_file_name(target_view.name, args.filename, filetype)
        try:
            logger.info(_("export.status").format(target_view))
            data = GetUrl.populate_data(server, target_view, filetype)
        except TSC.ServerResponseError as e:
            GetUrl.exit_with_error(logger, exception=e)
        try:
            with open(formatted_file_name, "wb") as f:
                logger.info(_("httputils.found_attachment").format(formatted_file_name))
                f.write(data)
                logger.info(_("export.success").format(args.url, formatted_file_name))
        except Exception as e:
            GetUrl.exit_with_error(logger, exception=e)

    @staticmethod
    def download_and_save_wb(logger, server, args, filetype):
        workbook = GetUrl.get_workbook_name(logger, args.url)
        logger.debug("Generating " + filetype + " for workbook " + workbook)
        formatted_file_name = GetUrl.set_file_name(workbook, args.filename, filetype)
        try:
            logger.info(_("export.status").format(args.url))
            target_workbook = GetUrl.get_wb_by_content_url(logger, server, workbook)
        except TSC.ServerResponseError as e:
            GetUrl.exit_with_error(logger, exception=e)
        try:
            logger.info(_("httputils.found_attachment").format(formatted_file_name))
            server.workbooks.download(target_workbook.id, filepath=formatted_file_name, no_extract=False)
            logger.info(_("export.success").format(args.url, formatted_file_name))
        except TSC.ServerResponseError as e:
            logger.debug("Error downloading workbook")
            GetUrl.exit_with_error(logger, exception=e)
