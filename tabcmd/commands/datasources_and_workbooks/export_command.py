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
        group = export_parser.add_argument_group(title=ExportCommand.name)
        group.add_argument("url", help="url of the workbook or view to export")
        export_parser_group = group.add_mutually_exclusive_group(required=True)
        export_parser_group.add_argument("--pdf", action="store_true", help=_("export.options.pdf"))
        export_parser_group.add_argument("--fullpdf", action="store_true", help=_("export.options.fullpdf"))
        export_parser_group.add_argument("--png", action="store_true", help=_("export.options.png"))
        export_parser_group.add_argument("--csv", action="store_true", help=_("export.options.csv"))

        group.add_argument(
            "--pagelayout",
            choices=["landscape", "portrait"],
            type=str.lower,
            default=None,
            help="page orientation (landscape or portrait) of the exported PDF",
        )
        group.add_argument(
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
            type=str.lower,
            default="letter",
            help="Set the page size of the exported PDF",
        )

        group.add_argument(
            "--width", default=800, help="[Not Yet Implemented] Set the width of the image in pixels. Default is 800 px"
        )
        group.add_argument("--filename", "-f", help="filename to store the exported data")
        group.add_argument("--height", default=600, help=_("export.options.height"))
        group.add_argument(
            "--filter",
            metavar="COLUMN=VALUE",
            help="Data filter to apply to the view",
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
        server = session.create_session(args, logger)
        view_content_url, wb_content_url = ExportCommand.parse_export_url_to_workbook_and_view(logger, args.url)
        logger.debug(["view_url:", view_content_url, "workbook:", wb_content_url])
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

        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response").format(""), e)
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)
        try:
            save_name = args.filename or default_filename
            if args.csv:
                ExportCommand.save_to_data_file(logger, output, save_name)
            else:
                ExportCommand.save_to_file(logger, output, save_name)

        except Exception as e:
            Errors.exit_with_error(logger, "Error saving to file", e)

    @staticmethod
    def apply_filters_from_args(request_options: TSC.PDFRequestOptions, args, logger=None) -> None:
        if args.filter:
            logger.debug("filter = {}".format(args.filter))
            params = args.filter.split("&")
            for value in params:
                ExportCommand.apply_filter_value(logger, request_options, value)

    # filtering isn't actually implemented for workbooks in REST
    @staticmethod
    def download_wb_pdf(server, workbook_item, args, logger):
        logger.debug(args.url)
        pdf_options = TSC.PDFRequestOptions(maxage=1)
        if args.filter or args.url.find("?") > 0:
            logger.info("warning: Filter values will not be applied when exporting a complete workbook")
        ExportCommand.apply_values_from_url_params(logger, pdf_options, args.url)
        ExportCommand.apply_pdf_options(logger, pdf_options, args)
        logger.debug(pdf_options.get_query_params())
        server.workbooks.populate_pdf(workbook_item, pdf_options)
        return workbook_item.pdf

    @staticmethod
    def download_view_pdf(server, view_item, args, logger):
        logger.debug(args.url)
        pdf_options = TSC.PDFRequestOptions(maxage=1)
        ExportCommand.apply_values_from_url_params(logger, pdf_options, args.url)
        ExportCommand.apply_filters_from_args(pdf_options, args, logger)
        ExportCommand.apply_pdf_options(logger, pdf_options, args)
        logger.debug(pdf_options.get_query_params())
        server.views.populate_pdf(view_item, pdf_options)
        return view_item.pdf

    @staticmethod
    def download_csv(server, view_item, args, logger):
        logger.debug(args.url)
        csv_options = TSC.CSVRequestOptions(maxage=1)
        ExportCommand.apply_values_from_url_params(logger, csv_options, args.url)
        ExportCommand.apply_filters_from_args(csv_options, args, logger)
        logger.debug(csv_options.get_query_params())
        server.views.populate_csv(view_item, csv_options)
        return view_item.csv

    @staticmethod
    def download_png(server, view_item, args, logger):
        logger.debug(args.url)
        image_options = TSC.ImageRequestOptions(maxage=1)
        ExportCommand.apply_values_from_url_params(logger, image_options, args.url)
        ExportCommand.apply_filters_from_args(image_options, args, logger)
        DatasourcesAndWorkbooks.apply_png_options(logger, image_options, args)
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
