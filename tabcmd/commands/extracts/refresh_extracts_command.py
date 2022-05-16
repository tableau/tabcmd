import tableauserverclient as TSC

from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.extracts.extracts_command import ExtractsCommand
from tabcmd.execution.logger_config import log
from tabcmd.commands.constants import Errors
from tabcmd import _

class RefreshExtracts(ExtractsCommand):

    name: str = "refreshextracts"
    description: str = _("refreshextracts.short_description")

    @staticmethod
    def define_args(refresh_extract_parser):
        target_group = refresh_extract_parser.add_mutually_exclusive_group(required=True)
        target_group.add_argument("-d", "--datasource")
        target_group.add_argument("-w", "--workbook")

        set_incremental_options(refresh_extract_parser)
        set_calculations_options(refresh_extract_parser)
        set_project_arg(refresh_extract_parser)
        set_parent_project_arg(refresh_extract_parser)
        refresh_extract_parser.add_argument(
            "--url",
            help=_("refreshextracts.options.url")
        )

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        refresh_action = "refresh"
        try:
            if args.datasource:
                logger.debug("Finding datasource `{}` on the server...".format(args.datasource))
                ExtractsCommand.print_task_scheduling_message(logger, "datasource", args.datasource, "refreshed")
                datasource_id = ExtractsCommand.get_data_source_id(logger, server, args.datasource)
                job = server.datasources.refresh(datasource_id)

            elif args.workbook:
                logger.debug("Finding workbook `{}` on the server...".format(args.workbook))
                ExtractsCommand.print_task_scheduling_message(logger, "workbook", args.workbook, "refreshed")
                workbook_id = ExtractsCommand.get_workbook_id(logger, server, args.workbook)
                job = server.workbooks.refresh(workbook_id)

        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, _("refreshextracts.errors.error"), e)
        ExtractsCommand.print_success_message(logger, refresh_action, job)
