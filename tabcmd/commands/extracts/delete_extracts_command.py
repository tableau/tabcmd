import tableauserverclient as TSC

from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.extracts.extracts_command import ExtractsCommand
from tabcmd.execution.logger_config import log
from tabcmd.execution.localize import _


class DeleteExtracts(ExtractsCommand):
    """
    Command to delete extracts for a published workbook or data source.
    """

    name: str = "deleteextracts"
    description: str = _("deleteextracts.short_description")

    @staticmethod
    def define_args(delete_extract_parser):
        set_ds_xor_wb_args(delete_extract_parser)
        set_embedded_datasources_options(delete_extract_parser)
        # set_encryption_option(delete_extract_parser)
        set_project_arg(delete_extract_parser)
        set_parent_project_arg(delete_extract_parser)
        delete_extract_parser.add_argument("--url", help=_("createextracts.options.url"))

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        try:
            if args.datasource:
                logger.info("Finding datasource `{}` on the server...".format(args.datasource))
                data_source_item = ExtractsCommand.get_data_source_item(logger, server, args.datasource)
                job = server.datasources.delete_extract(data_source_item)
            elif args.workbook:
                logger.info("Finding workbook `{}` on the server...".format(args.workbook))
                workbook_item = ExtractsCommand.get_workbook_item(logger, server, args.workbook)
                job = server.workbooks.delete_extract(workbook_item)
        except TSC.ServerResponseError as e:
            ExtractsCommand.exit_with_error(logger, _("deleteextracts.errors.error"), e)

        ExtractsCommand.print_success_message(logger, "deletion", job)
