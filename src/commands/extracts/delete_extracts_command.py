import tableauserverclient as TSC

from src.commands.auth.session import Session
from src.commands.constants import Errors
from src.commands.server import Server
from src.execution.global_options import *
from src.execution.localize import _
from src.execution.logger_config import log


class DeleteExtracts(Server):
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
                logger.info(_("deleteextracts.for.datasource").format(args.datasource))
                data_source_item = Server.get_data_source_item(logger, server, args.datasource)
                job = server.datasources.delete_extract(data_source_item)
            elif args.workbook:
                logger.info(_("deleteextracts.for.workbook_name").format(args.workbook))
                workbook_item = Server.get_workbook_item(logger, server, args.workbook)
                job = server.workbooks.delete_extract(workbook_item)
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, _("deleteextracts.errors.error"), e)

        logger.info(_("common.output.job_queued_success"))
        logger.debug("Extract deletion queued with JobID: {}".format(job.id))
