import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class CreateExtracts(Server):
    """
    Command that creates extracts for a published workbook or data source.
    """

    name: str = "createextracts"
    description: str = _("createextracts.short_description")

    @staticmethod
    def define_args(create_extract_parser):
        group = create_extract_parser.add_argument_group(title=CreateExtracts.name)
        set_ds_xor_wb_args(group)
        set_embedded_datasources_options(group)
        set_encryption_option(group)
        set_project_arg(group)
        set_parent_project_arg(group)
        set_site_url_arg(group)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)
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
        except Exception as e:

            if args.continue_if_exists and Errors.is_resource_conflict(e):
                logger.info(_("tabcmd.result.already_exists").format(_("content_type.extract"), args.name))
                return
            Errors.exit_with_error(logger, e)

        logger.info(_("common.output.job_queued_success"))
        logger.debug("Extract creation queued with JobID: {}".format(job.id))
