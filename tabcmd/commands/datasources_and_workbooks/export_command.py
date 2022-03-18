import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class ExportCommand(DatasourcesAndWorkbooks):

    name: str = "export"
    description: str = "Export the data or image of a view from the server"

    @staticmethod
    def get_content_url_for_workbook(url):
        # check the size of list
        separated_list = url.split("/")
        reversed_list = separated_list[::-1]
        return reversed_list[1]

    @staticmethod
    def get_content_url_for_view(url):
        # check the size of list
        separated_list = url.split("/")
        if len(separated_list) > 2:
            print("error")
        return "{}/sheets/{}".format(separated_list[0], separated_list[1])

    """
    Command to Export a view_name or workbook from Tableau Server and save
    it to a file. This command can also export just the data used for a view_name
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        logger.info("===== Requesting '{0}' from the server...".format(args.url))
        try:
            if args.fullpdf:  # it's a workbook
                workbook = ExportCommand.get_content_url_for_workbook(args.url)
                workbook_from_list = ExportCommand.get_wb_by_content_url(logger, server, workbook)
                req_option_pdf = TSC.PDFRequestOptions(maxage=1)
                server.workbooks.populate_pdf(workbook_from_list, req_option_pdf)
                output = workbook_from_list.pdf
                default_filename = "{}.pdf".format(workbook)

            elif args.pdf or args.png or args.csv:  # it's a view

                view = ExportCommand.get_content_url_for_view(args.url)
                views_from_list = ExportCommand.get_view_by_content_url(logger, server, view)

                if args.pdf:
                    req_option_pdf = TSC.PDFRequestOptions(maxage=1)
                    server.views.populate_pdf(views_from_list, req_option_pdf)
                    output = views_from_list.pdf
                    default_filename = "{}.pdf".format(views_from_list.name)

                elif args.csv:
                    req_option_csv = TSC.CSVRequestOptions(maxage=1)
                    server.views.populate_csv(views_from_list, req_option_csv)
                    output = views_from_list.csv
                    default_filename = "{}.csv".format(view)

                elif args.png:
                    req_option_csv = TSC.CSVRequestOptions(maxage=1)
                    server.views.populate_csv(views_from_list, req_option_csv)
                    output = views_from_list.png
                    default_filename = "{}.png".format(view)
            else:
                ExportCommand.exit_with_error(logger, "You must specify an export method")

        except TSC.ServerResponseError as e:
            ExportCommand.exit_with_error(logger, "Error exporting from server", e)
        try:
            ExportCommand.save_to_file(args, logger, output, default_filename)
        except TSC.ServerResponseError as e:
            ExportCommand.exit_with_error(logger, "Error saving to file", e)

    @staticmethod
    def save_to_file(args, logger, output, default_filename):
        file_name_with_path = args.filename or default_filename
        logger.info("===== Found attachment: {}".format(file_name_with_path))
        with open(file_name_with_path, "wb") as f:
            f.write(output)
            logger.info("===== Saved {0} to '{1}'".format(args.url, file_name_with_path))
