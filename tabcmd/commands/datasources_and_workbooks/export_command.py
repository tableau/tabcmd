import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from ..auth.session import Session
from tabcmd.parsers.export_parser import ExportParser
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class ExportCommand(DatasourcesAndWorkbooks):
    @classmethod
    def parse(cls):
        args, url = ExportParser.export_parser()
        return cls(args, url)

    @staticmethod
    def get_workbook(url):
        # check the size of list
        separated_list = url.split("/")
        reversed_list = separated_list[::-1]
        return reversed_list[1]

    @staticmethod
    def get_view(url):
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
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)

        if args.fullpdf:  # its a workbook
            workbook = ExportCommand.get_workbook(args.url)
            try:
                workbook_from_list = ExportCommand.get_wb_by_content_url(logger, server, workbook)
                req_option_pdf = TSC.PDFRequestOptions(maxage=1)
                server.workbooks.populate_pdf(workbook_from_list, req_option_pdf)
                if args.filename is None:
                    file_name_with_path = "{}.pdf".format(workbook)
                else:
                    file_name_with_path = args.filename
                formatted_file_name = file_name_with_path
                with open(formatted_file_name, "wb") as f:
                    f.write(workbook_from_list.pdf)
                    logger.info("Exported successfully")

            except TSC.ServerResponseError as e:
                ExportCommand.exit_with_error(logger, "Server Error:", e)

        elif args.pdf or args.png or args.csv:  # it's a view
            if args.pdf:
                view = ExportCommand.get_view(args.url)
                try:
                    views_from_list = ExportCommand.get_view_by_content_url(logger, server, view)
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
                    ExportCommand.exit_with_error(logger, "Server Error", e)
            if args.csv:
                view = ExportCommand.get_view(args.url)
                try:
                    views_from_list = ExportCommand.get_view_by_content_url(logger, server, view)
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
                    logger.error("Server error occurred")
            if args.png:
                view = ExportCommand.get_view(args.url)
                try:
                    views_from_list = ExportCommand.get_view_by_content_url(logger, server, view)
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
                    ExportCommand.exit_with_error(logger, "Server Error", e)

        else:
            ExportCommand.exit_with_error(logger, "You must specify an export method")
