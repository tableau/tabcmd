import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.extracts.extracts_command import ExtractsCommand
from tabcmd.execution.logger_config import log


class RefreshExtracts(ExtractsCommand):
    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        refresh_action = "refresh"
        if args.datasource:
            try:
                # TODO: this message should have the projects passed with the ds name
                # e.g instead of "regional" it should say "samples/regional"
                ExtractsCommand.print_plan_message(logger, "datasource", args.datasource, "refreshed")
                datasource_id = ExtractsCommand.get_data_source_id(server, args.datasource)
                job = server.datasources.refresh(datasource_id)
                ExtractsCommand.print_success_message(logger, refresh_action, job)
            except TSC.ServerResponseError as e:
                ExtractsCommand.exit_with_error(logger, e)

        elif args.workbook:
            try:
                ExtractsCommand.print_plan_message(logger, "workbook", args.workbook, "refreshed")
                workbook_id = ExtractsCommand.get_workbook_id(server, args.workbook)
                job = server.workbooks.refresh(workbook_id)
                ExtractsCommand.print_success_message(logger, refresh_action, job)
            except TSC.ServerResponseError as e:
                ExtractsCommand.exit_with_error(logger, e)
