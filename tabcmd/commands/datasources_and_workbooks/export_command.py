import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks

pagesize = TSC.PDFRequestOptions.PageType  # type alias for brevity


class ExportCommand(DatasourcesAndWorkbooks):

    name: str = "export"
    description: str = _("export.short_description")

    @staticmethod
    def define_args(export_parser):
        export_parser.add_argument("url", help="url of the workbook or view to export")
        export_parser_group = export_parser.add_mutually_exclusive_group(required=True)
        export_parser_group.add_argument("--pdf", action="store_true", help=_("export.options.pdf"))
        export_parser_group.add_argument("--fullpdf", action="store_true", help=_("export.options.fullpdf"))
        export_parser_group.add_argument("--png", action="store_true", help=_("export.options.png"))
        export_parser_group.add_argument("--csv", action="store_true", help=_("export.options.csv"))

        export_parser.add_argument(
            "--pagelayout",
            choices=["landscape", "portrait"],
            default=None,
            help="page orientation (landscape or portrait) of the exported PDF",
        )
        export_parser.add_argument(
            "--pagesize",
            choices=[
                pagesize.A3,
                pagesize.A4,
                pagesize.A5,
                pagesize.B4,
                pagesize.B5,
                pagesize.Executive,
                pagesize.Folio,
                pagesize.Ledger,
                pagesize.Legal,
                pagesize.Letter,
                pagesize.Note,
                pagesize.Quarto,
                pagesize.Tabloid,
                pagesize.Unspecified,
            ],
            default="letter",
            help="Set the page size of the exported PDF",
        )

        export_parser.add_argument(
            "--width", default=800, help="Set the width of the image in pixels. Default is 800 px"
        )
        export_parser.add_argument("--filename", "-f", help="filename to store the exported data")
        export_parser.add_argument("--height", default=600, help=_("export.options.height"))
        export_parser.add_argument(
            "--filter",
            metavar="COLUMN:VALUE",
            help="View filter to apply to the view",
        )

    """
    Command to Export a view_name or workbook from Tableau Server and save
    it to a file. This command can also export just the data used for a view_name
    """

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        view_content_url, wb_content_url = ExportCommand.parse_export_url_to_workbook_and_view(logger, args.url)
        logger.debug([view_content_url, wb_content_url])
        if not view_content_url and not wb_content_url:
            view_example = "/workbook_name/view_name"
            message = "{} [{}]".format(
                _("export.errors.requires_workbook_view_param").format(__class__.__name__), view_example
            )
            Errors.exit_with_error(logger, message)

        try:
            if args.fullpdf:  # it's a workbook
                workbook_item = ExportCommand.get_wb_by_content_url(logger, server, wb_content_url)
                output = ExportCommand.download_wb_pdf(server, workbook_item, args, logger)

                default_filename = "{}.pdf".format(workbook_item.name)

            elif args.pdf or args.png or args.csv:  # it's a view
                view_item = ExportCommand.get_view_by_content_url(logger, server, view_content_url)

                if args.pdf:
                    output = ExportCommand.download_view_pdf(server, view_item, args, logger)
                    default_filename = "{}.pdf".format(view_item.name)
                elif args.csv:
                    output = ExportCommand.download_csv(server, view_item, args, logger)
                    default_filename = "{}.csv".format(view_item.name)
                elif args.png:
                    output = ExportCommand.download_png(server, view_item, args, logger)

                    default_filename = "{}.png".format(view_item.name)

        except Exception as e:
            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response").format(""), e)

        try:
            save_name = args.filename or default_filename
            if args.csv:
                ExportCommand.save_to_data_file(logger, output, save_name)
            else:
                ExportCommand.save_to_file(logger, output, save_name)


        except Exception as e:
            Errors.exit_with_error(logger, "Error saving to file", e)

    @staticmethod
    def apply_values_from_args(request_options: TSC.PDFRequestOptions, args, logger=None) -> None:
        logger.debug(
            "Args: {}, {}, {}, {}, {}".format(args.pagelayout, args.pagesize, args.width, args.height, args.filter)
        )
        if args.pagelayout:
            request_options.orientation = args.pagelayout
        if args.pagesize:
            request_options.page_type = args.pagesize
        if args.filter:
            params = args.filter.split("&")
            for value in params:
                ExportCommand.apply_filter_value(request_options, value, logger)

    @staticmethod
    def download_wb_pdf(server, workbook_item, args, logger):
        logger.debug(args.url)
        pdf_options = TSC.PDFRequestOptions(maxage=1)
        ExportCommand.apply_values_from_url_params(pdf_options, args.url, logger)
        ExportCommand.apply_values_from_args(pdf_options, args, logger)
        logger.debug(pdf_options.get_query_params())
        server.workbooks.populate_pdf(workbook_item, pdf_options)
        return workbook_item.pdf

    @staticmethod
    def download_view_pdf(server, view_item, args, logger):
        logger.debug(args.url)
        pdf_options = TSC.PDFRequestOptions(maxage=1)
        ExportCommand.apply_values_from_url_params(pdf_options, args.url, logger)
        ExportCommand.apply_values_from_args(pdf_options, args, logger)
        logger.debug(pdf_options.get_query_params())
        server.views.populate_pdf(view_item, pdf_options)
        return view_item.pdf

    @staticmethod
    def download_csv(server, view_item, args, logger):
        logger.debug(args.url)
        csv_options = TSC.CSVRequestOptions(maxage=1)
        ExportCommand.apply_values_from_url_params(csv_options, args.url, logger)
        ExportCommand.apply_values_from_args(csv_options, args, logger)
        logger.debug(csv_options.get_query_params())
        server.views.populate_csv(view_item, csv_options)
        return view_item.csv

    @staticmethod
    def download_png(server, view_item, args, logger):
        logger.debug(args.url)
        image_options = TSC.ImageRequestOptions(maxage=1)
        ExportCommand.apply_values_from_url_params(image_options, args.url, logger)
        ExportCommand.apply_values_from_args(image_options, args, logger)
        DatasourcesAndWorkbooks.apply_png_options(image_options, args, logger)
        logger.debug(image_options.get_query_params())
        server.views.populate_image(view_item, image_options)
        return view_item.image

    @staticmethod
    def parse_export_url_to_workbook_and_view(logger, url):
        logger.info(_("export.status").format(url))
        if " " in url:
            Errors.exit_with_error(logger, _("export.errors.white_space_workbook_view"))
        if "?" in url:
            url = url.split("?")[0]
        # input should be workbook_name/view_name or /workbook_name/view_name
        url = url.lstrip("/")  # strip opening / if present
        if not url.find("/"):
            return None, None
        name_parts = url.split("/")
        if len(name_parts) != 2:
            return None, None
        workbook = name_parts[0]
        view = "{}/sheets/{}".format(workbook, name_parts[1])
        return view, workbook
