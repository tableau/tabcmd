import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class DeleteExtracts(Server):
    """
    Command to delete extracts for a published workbook or data source.
    """

    name: str = "deleteextracts"
    description: str = _("deleteextracts.short_description")

    @staticmethod
    def define_args(delete_extract_parser):
        group = delete_extract_parser.add_argument_group(title=DeleteExtracts.name)
        set_ds_xor_wb_args(group)
        set_embedded_datasources_options(group)
        # set_encryption_option(group)
        set_project_arg(group)
        set_parent_project_arg(group)
        group.add_argument("--url", help=_("createextracts.options.url"))

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
        except Exception as e:
            Errors.exit_with_error(logger, e)

        logger.info(_("common.output.job_queued_success"))
        logger.debug("Extract deletion queued with JobID: {}".format(job.id))
