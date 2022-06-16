import tableauserverclient as TSC

from src.commands.auth.session import Session
from src.commands.constants import Errors
from src.commands.server import Server
from src.execution.global_options import *
from src.execution.localize import _
from src.execution.logger_config import log


class CreateExtracts(Server):
    """
    Command that creates extracts for a published workbook or data source.
    """

    name: str = "createextracts"
    description: str = _("createextracts.short_description")

    @staticmethod
    def define_args(create_extract_parser):
        set_ds_xor_wb_args(create_extract_parser)
        set_embedded_datasources_options(create_extract_parser)
        set_encryption_option(create_extract_parser)
        set_project_arg(create_extract_parser)
        set_parent_project_arg(create_extract_parser)
        set_site_url_arg(create_extract_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        creation_call = None
        try:
            logger.debug(
                "Extract params: encrypt={}, include_all={}, datasources={}".format(
                    args.encrypt, args.include_all, args.embedded_datasources
                )
            )

            if args.datasource:
                data_source_item = Server.get_data_source_item(logger, server, args.datasource)
                logger.info(_("createextracts.for.datasource").format(args.datasource))
                job = server.datasources.create_extract(data_source_item, encrypt=args.encrypt)

            elif args.workbook:
                workbook_item = Server.get_workbook_item(logger, server, args.workbook)
                logger.info(_("createextracts.for.workbook_name").format(args.workbook))
                job = server.workbooks.create_extract(
                    workbook_item,
                    encrypt=args.encrypt,
                    includeAll=args.include_all,
                    datasources=args.embedded_datasources,
                )
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, exception=e)

        logger.info(_("common.output.job_queued_success"))
        logger.debug("Extract creation queued with JobID: {}".format(job.id))
