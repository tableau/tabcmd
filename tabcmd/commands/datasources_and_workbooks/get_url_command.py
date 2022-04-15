import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks
from tabcmd.execution.global_options import *


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
        file_type = GetUrl.get_download_type(logger, args.filename, args.url)
        logger.debug("Getting file type " + file_type)
        if file_type in ["pdf", "png", "csv"]:
            GetUrl.download_and_save_view(logger, server, args, file_type)
        elif file_type == "twbx" or file_type == "twb":
            GetUrl.download_and_save_wb(logger, server, args, file_type)
        else:
            GetUrl.exit_with_error(logger, "The url must include a file extension")

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
                GetUrl.exit_with_error(logger, "The url must include a file extension")
        return type_of_file

    @staticmethod
    def get_name_without_possible_extension(filename):
        split_parts = filename.split(".")
        return split_parts[0]

    @staticmethod
    def get_workbook_name(url):
        separated_list = url.split("/")
        workbook_name = GetUrl.get_name_without_possible_extension(separated_list[2])
        return workbook_name

    @staticmethod
    def get_view_url(url):
        # check the size of list
        separated_list = url.split("/")
        workbook_name = separated_list[2]
        view_name = GetUrl.get_name_without_possible_extension(separated_list[::-1][0])
        return "{}/sheets/{}".format(workbook_name, view_name)

    @staticmethod
    def get_target_view(args, logger, server):
        try:
            view = GetUrl.get_view_url(args.url)
        except Exception as e:
            GetUrl.exit_with_error(logger, "Could not get contenturl for view", e)
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
            GetUrl.exit_with_error("Unknown filetype")

    @staticmethod
    def download_and_save_view(logger, server, args, filetype):
        target_view = GetUrl.get_target_view(args, logger, server)
        formatted_file_name = GetUrl.set_file_name(target_view.name, args.filename, filetype)
        try:
            logger.info("===== Requesting '{}' from the server...".format(target_view))
            data = GetUrl.populate_data(server, target_view, filetype)
        except TSC.ServerResponseError as e:
            GetUrl.exit_with_error(logger, exception=e)
        try:
            with open(formatted_file_name, "wb") as f:
                logger.info("===== Found attachment: {}".format(formatted_file_name))
                f.write(data)
                logger.info("===== Saved {} to '{}'".format(args.url, formatted_file_name))
        except Exception as e:
            GetUrl.exit_with_error(logger, exception=e)

    @staticmethod
    def download_and_save_wb(logger, server, args, filetype):
        workbook = GetUrl.get_workbook_name(args.url)
        logger.debug("Generating " + filetype + " for workbook " + workbook)
        formatted_file_name = GetUrl.set_file_name(workbook, args.filename, filetype)
        try:
            logger.info("===== Requesting '{}' from the server...".format(args.url))
            target_workbook = GetUrl.get_wb_by_content_url(logger, server, workbook)
        except TSC.ServerResponseError as e:
            GetUrl.exit_with_error(logger, exception=e)
        try:
            logger.info("===== Found attachment: {}".format(formatted_file_name))
            server.workbooks.download(target_workbook.id, filepath=formatted_file_name, no_extract=False)
            logger.info("===== Saved {} to '{}'".format(args.url, formatted_file_name))
        except TSC.ServerResponseError as e:
            logger.debug("Error downloading workbook")
            GetUrl.exit_with_error(logger, exception=e)
