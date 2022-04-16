import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks
from tabcmd.commands.constants import Errors

class ExportCommand(DatasourcesAndWorkbooks):

    name: str = "export"
    description: str = "Export the data or image of a view from the server"

    @staticmethod
    def define_args(export_parser):
        export_parser.add_argument("url", help="url of the workbook or view to export")
        export_parser_group = export_parser.add_mutually_exclusive_group(required=True)
        export_parser_group.add_argument("--pdf", action="store_true", help="pdf of a view")
        export_parser_group.add_argument("--fullpdf", action="store_true", help="fullpdf of workbook")
        export_parser_group.add_argument("--png", action="store_true", help="png of a view")
        export_parser_group.add_argument("--csv", action="store_true", help="csv of a view")

        export_parser.add_argument(
            "--pagelayout",
            choices=["landscape", "portrait"],
            default="landscape",
            help="page orientation (landscape or portrait) of the exported PDF",
        )
        export_parser.add_argument("--pagesize", default="letter", help="Set the page size of the exported PDF")
        export_parser.add_argument("--width", default=800, help="Set the width in pixels. Default is 800 px")
        export_parser.add_argument("--filename", "-f", help="filename to store the exported data")
        export_parser.add_argument("--height", default=600, help="Sets the height in pixels. Default is 600 px")
        export_parser.add_argument(
            "--filter",
            "-vf",
            metavar="COLUMN:VALUE",
            help="View filter to apply to the view",
        )

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
        view_content_url, wb_content_url = ExportCommand.parse_url_to_workbook_and_view(args.url)
        logger.debug("Parsed to {}, {}".format(wb_content_url, view_content_url))
        if args.fullpdf:  # it's a workbook
            try:
                workbook_item = ExportCommand.get_wb_by_content_url(logger, server, wb_content_url)
            except Exception as e:
                Errors.exit_with_error(logger, "Error getting workbook info from server", e)

            try:
                req_option_pdf = TSC.PDFRequestOptions(maxage=1)
                server.workbooks.populate_pdf(workbook_item, req_option_pdf)
            except Exception as e:
                Errors.exit_with_error(logger, "Error downloading workbook pdf")
            output = workbook_item.pdf
            filename = "{}.pdf".format(wb_content_url)

        elif args.pdf or args.png or args.csv:  # it's a view
            try:
                view_item = ExportCommand.get_view_by_content_url(logger, server, view_content_url)
            except Exception as e:
                Errors.exit_with_error(logger, "Error getting view info from server", e)

            try:
                if args.pdf:
                    output = ExportCommand.download_pdf(server, view_item)
                    filename = "{}.pdf".format(view_item.name)
                elif args.csv:
                    output = ExportCommand.download_csv(server, view_item)
                    filename = "{}.csv".format(view_content_url)
                elif args.png:
                    output = ExportCommand.download_png(server, view_item)
                    filename = "{}.png".format(view_content_url)
            except Exception as e:
                Errors.exit_with_error(logger, "Error downloading view from server", e)

        else:
            ExportCommand.exit_with_error(logger, "You must specify an export method")

        try:
            save_name = args.filename or filename
            ExportCommand.save_to_file(logger, output, save_name)
            logger.info("===== Saved {0} to '{1}'".format(args.url, save_name))

        except Exception as e:
            Errors.exit_with_error(logger, "Error saving to file", e)


    @staticmethod
    def download_pdf(server, view_item):
        pdf = TSC.PDFRequestOptions(maxage=1)
        server.views.populate_pdf(view_item, pdf)
        return view_item.pdf

    @staticmethod
    def download_csv(server, view_item):
        csv = TSC.CSVRequestOptions(maxage=1)
        server.views.populate_csv(view_item, csv)
        return view_item.csv

    @staticmethod
    def download_png(server, view_item):
        # why does this call csv stuff?
        req_option_csv = TSC.CSVRequestOptions(maxage=1)
        server.views.populate_csv(view_item, req_option_csv)
        return view_item.png

    @staticmethod
    def parse_url_to_workbook_and_view(url):
        # input should be workbook_name/view_name
        if not url.find("/"):
            return None, None
        name_parts = url.split("/")
        if len(name_parts) != 2:
            return None, None
        workbook = name_parts[0]
        view = "{}/sheets/{}".format(workbook, name_parts[1])
        return view, workbook

    @staticmethod
    def save_to_file(logger, output, filename):
        logger.info("===== Found attachment: {}".format(filename))
        with open(filename, "wb") as f:
            f.write(output)
