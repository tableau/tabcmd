import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks
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
        get_url_parser.add_argument("url", help="url that identifies the view or workbook to export")
        set_filename_arg(get_url_parser)
        # TODO add args for png size in pixels, refresh
        # to send to the server these are both just set on the url?

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        file_type = GetUrl.evaluate_file_name(logger, args.filename, args.url)
        source_type = GetUrl.evaluate_source_type(args.url)
        if source_type == "workbooks":
            if file_type == "twbx" or file_type == "twb":
                GetUrl.generate_twb(logger, server, args)
            else:
                Errors.exit_with_error(logger,
                                       "Error: Workbooks can only be downloaded as twb or twbx files.")

        elif source_type == "views":
            view_url = ""
            try:
                view_url = GetUrl.get_view_url(args.url)
                view = GetUrl.get_view_by_content_url(logger, server, view_url)
            except Exception as e:
                Errors.exit_with_error(logger, "Error finding view {}".format(view_url), e)
            try:
                if file_type == "pdf":
                    req_option_pdf = TSC.PDFRequestOptions(maxage=1)
                    server.views.populate_pdf(view, req_option_pdf)
                    file_name_with_path = GetUrl.generate_file_name(args, view, "pdf")
                    output = view.pdf

                elif file_type == "png":
                    req_option_csv = TSC.CSVRequestOptions(maxage=1)
                    server.views.populate_csv(view, req_option_csv)
                    file_name_with_path = GetUrl.generate_file_name(args, view, "png")
                    output = view.png

                elif file_type == "csv":
                    req_option_csv = TSC.CSVRequestOptions(maxage=1)
                    server.views.populate_csv(view, req_option_csv)
                    file_name_with_path = GetUrl.generate_file_name(args, view, "csv")
                    output = view.csv

                else:
                    Errors.exit_with_error(logger,
                                           "Error: Views can only be retrieved as png, pdf or csv.")
            except TSC.ServerResponseError as e:
                Errors.exit_with_error(logger, "Error exporting from server", e)
            try:
                with open(file_name_with_path, "wb") as f:
                    f.write(output)
                    logger.info("Exported successfully")

            except TSC.ServerResponseError as e:
                Errors.exit_with_error(logger, "Error saving to file", e)

        else:
            Errors.exit_with_error(logger, "Invalid url - it should start with /views/ or /workbooks/")

    @staticmethod
    def evaluate_file_name(logger, file_name, url):
        type_of_file = None
        if file_name is not None:
            split_file_name = file_name.split(".")
            type_of_file = split_file_name[1]
        else:  # file_name is None:
            # grab from url
            split_url_to_get_extension = url.split(".")
            if len(split_url_to_get_extension) > 1:
                type_of_file = split_url_to_get_extension[1]
            else:
                Errors.exit_with_error(logger, "Error: File extension not found")
        return type_of_file

    @staticmethod
    def evaluate_source_type(url):
        return url.split("/")[1]

    @staticmethod
    def check_if_extension_present(name):
        extension = name.split(".")[1]
        # strip any query params
        extension = extension.split("?")[0]
        return extension in ["pdf", "csv", "png", "twb", "twbx"]

    @staticmethod
    def strip_extension_from_name(item_name):
        name_parts = item_name.split(".")
        return name_parts[0]

    @staticmethod
    def get_workbook_name(url):
        # "/workbooks/wb-name/view-name" --> "wb-name"
        separated_list = url.split("/")
        return separated_list[2]

    @staticmethod
    def get_view_url(url):
        # "/views/wb-name/view-name" --> "wb-name/sheets/view-name"
        separated_list = url.split("/")
        if len(separated_list) < 4:
            Errors.exit_with_error("Invalid view url `{}`".format(url))
        workbook_name = separated_list[2]
        view_name = separated_list[3]
        if GetUrl.check_if_extension_present(view_name):
            view_name = GetUrl.strip_extension_from_name(view_name)
        return "{}/sheets/{}".format(workbook_name, view_name)

    @staticmethod
    def generate_file_name(args, view, extension):
        if args.filename is None:
            file_name_with_path = "{}.{}".format(view.name, extension)
        else:
            file_name_with_path = args.filename
        return file_name_with_path

    @staticmethod
    def generate_twb(logger, server, args):
        workbook_name = GetUrl.get_workbook_name(args.url)
        try:
            target_workbook = GetUrl.get_wb_by_content_url(logger, server, workbook_name)
            server.workbooks.download(target_workbook.id, filepath=None, no_extract=False)
            logger.info("Workbook {} exported".format(target_workbook.name))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Server error:", e)
