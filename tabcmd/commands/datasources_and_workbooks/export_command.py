import tableauserverclient as TSC

from uuid import UUID

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks
from .datasources_workbooks_views_url_parser import DatasourcesWorkbooksAndViewsUrlParser

pagesize = TSC.PDFRequestOptions.PageType  # type alias for brevity
pageorientation = TSC.PDFRequestOptions.Orientation
imageresolution = TSC.ImageRequestOptions.Resolution
ImageResolutionStandard = "standard"


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
            choices=[pageorientation.Landscape, pageorientation.Portrait],
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

        group.add_argument("--width", default=800, help=_("export.options.width"))
        group.add_argument("--filename", "-f", help="filename to store the exported data")
        group.add_argument("--height", default=600, help=_("export.options.height"))
        group.add_argument(
            "--filter",
            metavar="COLUMN=VALUE",
            help="Data filter to apply to the view",
        )
        group.add_argument(
            "--resolution",
            choices=[imageresolution.High, ImageResolutionStandard],
            type=str.lower,
            help=_("export.options.resolution"),
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
        (
            view_content_url,
            wb_content_url,
            custom_view_id,
            custom_view_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.parse_export_url_to_workbook_view_and_custom_view(logger, args.url)
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

            elif args.pdf or args.png or args.csv:  # it's a view or custom_view
                (
                    export_item,
                    server_content_type,
                ) = DatasourcesWorkbooksAndViewsUrlParser.get_export_item_and_server_content_type_from_export_url(
                    view_content_url, logger, server, custom_view_id
                )

                if args.pdf:
                    output = ExportCommand.download_view_pdf(server_content_type, export_item, args, logger)
                    default_filename = "{}.pdf".format(export_item.name)
                elif args.csv:
                    output = ExportCommand.download_csv(server_content_type, export_item, args, logger)
                    default_filename = "{}.csv".format(export_item.name)
                elif args.png:
                    output = ExportCommand.download_png(server_content_type, export_item, args, logger)
                    default_filename = "{}.png".format(export_item.name)

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
    def apply_filters_from_args(request_options: TSC.RequestOptions, args, logger=None) -> None:
        if args.filter:
            logger.debug("filter = {}".format(args.filter))
            params = args.filter.split("&")
            for value in params:
                ExportCommand.apply_filter_value(logger, request_options, value)

    @staticmethod
    def download_wb_pdf(server, workbook_item, args, logger):
        logger.debug(args.url)
        pdf_options = TSC.PDFRequestOptions(maxage=1)
        ExportCommand.apply_values_from_url_params(logger, pdf_options, args.url)
        ExportCommand.apply_filters_from_args(pdf_options, args, logger)
        ExportCommand.apply_pdf_options(logger, pdf_options, args)
        logger.debug(pdf_options.get_query_params())
        server.workbooks.populate_pdf(workbook_item, pdf_options)
        return workbook_item.pdf

    @staticmethod
    def download_view_pdf(server_content_type, export_item, args, logger):
        logger.debug(args.url)
        pdf_options = TSC.PDFRequestOptions(maxage=1)
        ExportCommand.apply_values_from_url_params(logger, pdf_options, args.url)
        ExportCommand.apply_filters_from_args(pdf_options, args, logger)
        ExportCommand.apply_pdf_options(logger, pdf_options, args)
        logger.debug(pdf_options.get_query_params())
        server_content_type.populate_pdf(export_item, pdf_options)
        return export_item.pdf

    @staticmethod
    def download_csv(server_content_type, export_item, args, logger):
        logger.debug(args.url)
        csv_options = TSC.CSVRequestOptions(maxage=1)
        ExportCommand.apply_values_from_url_params(logger, csv_options, args.url)
        ExportCommand.apply_filters_from_args(csv_options, args, logger)
        logger.debug(csv_options.get_query_params())
        server_content_type.populate_csv(export_item, csv_options)
        return export_item.csv

    @staticmethod
    def download_png(server_content_type, export_item, args, logger):
        logger.debug(args.url)
        image_options = TSC.ImageRequestOptions(maxage=1)
        ExportCommand.apply_values_from_url_params(logger, image_options, args.url)
        ExportCommand.apply_filters_from_args(image_options, args, logger)
        DatasourcesAndWorkbooks.apply_png_options(logger, image_options, args)
        logger.debug(image_options.get_query_params())
        server_content_type.populate_image(export_item, image_options)
        return export_item.image
