import tableauserverclient as TSC

from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.extracts.extracts_command import ExtractsCommand
from tabcmd.execution.logger_config import log
from tabcmd.commands.constants import Errors


class CreateExtracts(ExtractsCommand):
    """
    Command that creates extracts for a published workbook or data source.
    """

    name: str = "createextracts"
    description: str = "Create extracts for a published workbook or data source"

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
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        try:
            if args.datasource:
                logger.debug("Finding datasource `{}` on the server...".format(args.datasource))
                ExtractsCommand.print_task_scheduling_message(logger, "datasource", args.workbook, "created")
                data_source_item = ExtractsCommand.get_data_source_item(logger, server, args.datasource)
                job = server.datasources.create_extract(data_source_item, encrypt=args.encrypt)

            elif args.workbook:
                logger.debug("Finding workbook `{}` on the server...".format(args.workbook))
                ExtractsCommand.print_task_scheduling_message(logger, "workbook", args.workbook, "created")
                workbook_item = ExtractsCommand.get_workbook_item(logger, server, args.workbook)
                logger.debug("Workbook: {}".format(workbook_item))
                logger.debug(
                    "Extract params: encrypt={}, include_all={}, datasources={}".format(
                        args.encrypt, args.include_all, args.embedded_datasources
                    )
                )
                job = server.workbooks.create_extract(
                    workbook_item,
                    encrypt=args.encrypt,
                    includeAll=args.include_all,
                    datasources=args.embedded_datasources,
                )
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Error creating extracts", e)

        ExtractsCommand.print_success_message(logger, "creation", job)
