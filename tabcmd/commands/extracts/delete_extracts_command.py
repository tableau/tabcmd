import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.extracts.extracts import Extracts
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
        set_ds_xor_wb_args(group, True)
        set_embedded_datasources_options(group)
        set_project_arg(group)
        set_parent_project_arg(group)

    @classmethod
    def run_command(cls, args):
        logger = log(cls.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)
        try:
            item = Extracts.get_wb_or_ds_for_extracts(args, logger, server)
            job: TSC.JobItem
            if args.datasource:
                logger.info(_("deleteextracts.for.datasource").format(args.datasource))
                job = server.datasources.delete_extract(item)
            else:
                if not args.include_all and not args.embedded_datasources:
                    Errors.exit_with_error(
                        logger,
                        _("extracts.workbook.errors.requires_datasources_or_include_all").format("deleteextracts"),
                    )
                logger.info(_("deleteextracts.for.workbook_name").format(args.workbook))
                job = server.workbooks.delete_extract(
                    item, includeAll=args.include_all, datasources=args.embedded_datasources
                )

        except Exception as e:
            Errors.exit_with_error(logger, exception=e)

        logger.info(_("common.output.job_queued_success"))
        logger.debug("Extract deletion queued with JobID: {}".format(job.id))
