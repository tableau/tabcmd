import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class GetUrl(DatasourcesAndWorkbooks):
    """
    This command gets the resource from Tableau Server that's represented
    by the specified (partial) URL. The result is returned as a file.
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        file_type = GetUrl.evaluate_file_name(logger, args.filename, args.url)
        if file_type == "pdf":
            GetUrl.generate_pdf(logger, server, args)
        elif file_type == "png":
            GetUrl.generate_png(logger, server, args)
        elif file_type == "csv":
            GetUrl.generate_csv(logger, server, args)
        elif file_type == "twbx" or file_type == "twb":
            GetUrl.generate_twb(logger, server, args)
        else:
            GetUrl.exit_with_error(logger, "Error file extension not found")

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
                GetUrl.exit_with_error(logger, "File extension not found")
        return type_of_file

    @staticmethod
    def check_if_extension_present(view_name):
        split_view = view_name.split(".")
        if len(split_view) == 2:
            return split_view[1] in ["pdf", "csv", "png", "twb", "twbx"]
        return False

    @staticmethod
    def get_view_without_extension(view_name):
        split_view = view_name.split(".")
        return split_view[0]

    @staticmethod
    def get_workbook(url):
        separated_list = url.split("/")
        if GetUrl.check_if_extension_present(separated_list[::-1][0]):
            view_second_half_url = GetUrl.get_view_without_extension(separated_list[::-1][0])
        else:
            view_second_half_url = separated_list[2]
        return view_second_half_url

    @staticmethod
    def get_view(url):
        # check the size of list
        separated_list = url.split("/")
        if GetUrl.check_if_extension_present(separated_list[::-1][0]):
            view_second_half_url = GetUrl.get_view_without_extension(separated_list[::-1][0])
        else:
            view_second_half_url = separated_list[2]
        return "{}/sheets/{}".format(separated_list[1], view_second_half_url)

    @staticmethod
    def generate_pdf(logger, server, args):
        view = GetUrl.get_view(args.url)
        try:
            views_from_list = GetUrl.get_view_by_content_url(logger, server, view)
            req_option_pdf = TSC.PDFRequestOptions(maxage=1)
            server.views.populate_pdf(views_from_list, req_option_pdf)
            if args.filename is None:
                file_name_with_path = "{}.pdf".format(views_from_list.name)
            else:
                file_name_with_path = args.filename
            formatted_file_name = file_name_with_path
            with open(formatted_file_name, "wb") as f:
                f.write(views_from_list.pdf)
                logger.info("Exported successfully")
        except TSC.ServerResponseError as e:
            GetUrl.exit_with_error(logger, "Server error:", e)

    @staticmethod
    def generate_png(logger, server, args):
        view = GetUrl.get_view(args.url)
        try:
            views_from_list = GetUrl.get_view_by_content_url(logger, server, view)
            req_option_csv = TSC.CSVRequestOptions(maxage=1)
            server.views.populate_csv(views_from_list, req_option_csv)
            if args.filename is None:
                file_name_with_path = "{}.png".format(view)
            else:
                file_name_with_path = args.filename
            formatted_file_name = file_name_with_path
            with open(formatted_file_name, "wb") as f:
                f.write(views_from_list.png)
                logger.info("Exported successfully")
        except TSC.ServerResponseError as e:
            GetUrl.exit_with_error(logger, "Server error:", e)

    @staticmethod
    def generate_csv(logger, server, args):
        view = GetUrl.get_view(args.url)
        try:
            views_from_list = GetUrl.get_view_by_content_url(logger, server, view)
            req_option_csv = TSC.CSVRequestOptions(maxage=1)
            server.views.populate_csv(views_from_list, req_option_csv)
            if args.filename is None:
                file_name_with_path = "{}.csv".format(view)
            else:
                file_name_with_path = args.filename
            formatted_file_name = file_name_with_path
            with open(formatted_file_name, "wb") as f:
                f.write(views_from_list.csv)
                logger.info("Exported successfully")
        except TSC.ServerResponseError as e:
            GetUrl.exit_with_error(logger, "Server error:", e)

    @staticmethod
    def generate_twb(logger, server, args):
        workbook = GetUrl.get_workbook(args.url)
        try:
            target_workbook = GetUrl.get_view_by_content_url(logger, server, workbook)
            server.workbooks.download(target_workbook.id, filepath=None, no_extract=False)
            logger.info("Workbook {} exported".format(target_workbook.name))
        except TSC.ServerResponseError as e:
            GetUrl.exit_with_error(logger, "Server error:", e)
