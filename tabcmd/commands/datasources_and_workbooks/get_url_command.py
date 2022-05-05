import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks
from tabcmd.commands.datasources_and_workbooks.export_command import ExportCommand
from tabcmd.execution.global_options import *
from tabcmd.commands.constants import Errors


class GetUrl(DatasourcesAndWorkbooks):
    """
    This command gets the resource from Tableau Server that's represented
    by the specified (partial) URL. The result is returned as a file.
    """

    name: str = "get"
    description: str = "Get a file from the server"

    @staticmethod
    def define_args(get_url_parser):
        get_url_parser.add_argument(
            "url",
            help="url that identifies the view or workbook to export\n"
            "e.g: /workbooks/workbook-name.twbx or views/view-name.pdf",
        )
        set_filename_arg(get_url_parser)
        # these don't need arguments, although that would be a good future addition
        # tabcmd get "/views/Finance/InvestmentGrowth.png?:size=640,480" -f growth.png
        # tabcmd get "/views/Finance/InvestmentGrowth.png?:refresh=yes" -f growth.png

    @staticmethod
    def run_command(args):
        # A view can be returned in PDF, PNG, or CSV (summary data only) format.
        # A Tableau workbook is returned as a TWB if it connects to a datasource/live connection,
        # or a TWBX if it uses an extract.
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        file_type = GetUrl.get_file_type_from_filename(logger, args.filename, args.url)
        content_type = GetUrl.evaluate_content_type(logger, args.url)
        if content_type == "workbook":
            if file_type == "twbx" or file_type == "twb":
                GetUrl.generate_twb(logger, server, args, file_type)
            else:
                Errors.exit_with_error(logger, message="A workbook can only be exported as twb or twbx")
        else:  # content type = view
            if file_type == "pdf":
                GetUrl.generate_pdf(logger, server, args)
            elif file_type == "png":
                GetUrl.generate_png(logger, server, args)
            elif file_type == "csv":
                GetUrl.generate_csv(logger, server, args)
            else:
                Errors.exit_with_error(logger, message="No valid file extension found in url or filename")

    @staticmethod
    def evaluate_content_type(logger, url):
        # specify a view to get using "/views/<workbookname>/<viewname>.<extension>"
        # specify a workbook to get using "/workbooks/<workbookname>.<extension>".
        if url.find("/views/") == 0:
            return "view"
        elif url.find("/workbooks/") == 0:
            return "workbook"
        else:
            Errors.exit_with_error(
                logger,
                message="Content url must be in the format /views/workbook-name/view-name or /workbooks/workbook-name",
            )

    @staticmethod
    def get_file_type_from_filename(logger, file_name, url):
        type_of_file = None

        if file_name:
            logger.debug("Get file type from filename: {}".format(file_name))
            type_of_file = GetUrl.get_file_extension(file_name)
        else:
            logger.debug("Get file type from url: {}".format(url))
            if url and url.find(".") > 0:
                type_of_file = GetUrl.get_file_extension(url)

        if not type_of_file:
            Errors.exit_with_error(logger, "The url must include a file extension if no filename is specified")

        logger.debug("extension from command line is {}".format(type_of_file))
        if type_of_file in ["pdf", "csv", "png", "twb", "twbx"]:
            logger.debug("Valid file type")
            return type_of_file

        Errors.exit_with_error(logger, "The file type {} is invalid".format(type_of_file))

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
    def strip_extension(filename):
        if filename.find(".") > 0:
            filename = filename.split(".")[0]
        return filename

    @staticmethod
    def get_workbook_name(logger, url):  # /workbooks/wb-name" -> "wb-name"
        name_parts = url.split("/")
        workbook_name = name_parts[::-1][0]  # last part
        workbook_name = GetUrl.strip_query_params(workbook_name)
        workbook_name = GetUrl.strip_extension(workbook_name)
        return workbook_name

    @staticmethod
    def get_view_url(url):  # "/views/wb-name/view-name" -> wb-name/sheets/view-name
        name_parts = url.split("/")  # ['', 'views', 'wb-name', 'view-name']
        if len(name_parts) != 4:
            raise ValueError("The url given did not match the expected format: 'views/workbook-name/view-name'")
        view_name = name_parts[::-1][0]
        view_name = GetUrl.strip_query_params(view_name)
        view_name = GetUrl.strip_extension(view_name)

        workbook_name = name_parts[2]
        return "{}/sheets/{}".format(workbook_name, view_name)

    @staticmethod
    def filename_from_args(file_argument, item_name, filetype):
        if file_argument is None:
            file_argument = "{}.{}".format(item_name, filetype)
        return file_argument

    @staticmethod
    def generate_pdf(logger, server, args):
        view_url = GetUrl.get_view_url(args.url)
        try:
            view_item: TSC.ViewItem = GetUrl.get_view_by_content_url(logger, server, view_url)
            logger.debug("Fetched view item {}".format(view_item.name))
            req_option_pdf = TSC.PDFRequestOptions(maxage=1)
            server.views.populate_pdf(view_item, req_option_pdf)
            filename = GetUrl.filename_from_args(args.filename, view_item.name, ".pdf")
            with open(filename, "wb") as f:
                f.write(view_item.pdf)
            logger.info("Saved {} to '{}'".format(args.url, filename))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Server error:", e)

    @staticmethod
    def generate_png(logger, server, args):
        view = GetUrl.get_view_url(args.url)
        try:
            view_item: TSC.ViewItem = GetUrl.get_view_by_content_url(logger, server, view)
            req_option_csv = TSC.CSVRequestOptions(maxage=1)
            server.views.populate_csv(view_item, req_option_csv)
            filename = GetUrl.filename_from_args(args.filename, view_item.name, ".png")
            with open(filename, "wb") as f:
                f.write(view_item.png)
            logger.info("Saved {} to '{}'".format(args.url, filename))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Server error:", e)

    @staticmethod
    def generate_csv(logger, server, args):
        view_url = GetUrl.get_view_url(args.url)
        try:
            view_item: TSC.ViewItem = GetUrl.get_view_by_content_url(logger, server, view_url)
            req_option_csv = TSC.CSVRequestOptions(maxage=1)
            server.views.populate_csv(view_item, req_option_csv)
            file_name_with_path = GetUrl.filename_from_args(args.filename, view_item.name, ".csv")
            with open(file_name_with_path, "wb") as f:
                f.write(view_item.csv)
            logger.info("Saved {} to '{}'".format(args.url, file_name_with_path))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Server error:", e)

    @staticmethod
    def generate_twb(logger, server, args, file_extension):
        workbook_name = GetUrl.get_workbook_name(logger, args.url)
        try:
            target_workbook = GetUrl.get_wb_by_content_url(logger, server, workbook_name)
            file_name_with_path = GetUrl.filename_from_args(args.filename, workbook_name, file_extension)
            server.workbooks.download(target_workbook.id, filepath=file_name_with_path, no_extract=False)
            logger.info("Saved {} to '{}'".format(args.url, file_name_with_path))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Server error:", e)
