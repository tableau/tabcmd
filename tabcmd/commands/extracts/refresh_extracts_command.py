import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.extracts.extracts_command import ExtractsCommand
from tabcmd.execution.logger_config import log


class RefreshExtracts(ExtractsCommand):

    name: str = "refreshextracts"
    description: str = "Refresh the extracts of a workbook or datasource on the server"

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
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
            ExtractsCommand.exit_with_error(logger, "Error refreshing extracts", e)
        ExtractsCommand.print_success_message(logger, refresh_action, job)
