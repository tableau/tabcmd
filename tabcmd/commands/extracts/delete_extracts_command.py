import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.extracts.extracts_command import ExtractsCommand
from tabcmd.execution.logger_config import log


class DeleteExtracts(ExtractsCommand):
    """
    Command to delete extracts for a published workbook or data source.
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        if args.datasource:
            try:
                data_source_item = ExtractsCommand.get_data_source_item(server, args.datasource)
                job = server.datasources.delete_extract(data_source_item)
                ExtractsCommand.print_success_message(logger, "deletion", job)
            except TSC.ServerResponseError as e:
                ExtractsCommand.exit_with_error(logger, "Server Error:", e)
        elif args.workbook:
            try:
                workbook_item = ExtractsCommand.get_workbook_item(server, args.workbook)
                job = server.workbooks.delete_extract(workbook_item)
                ExtractsCommand.print_success_message(logger, "deletion", job)
            except TSC.ServerResponseError as e:
                ExtractsCommand.exit_with_error(logger, "Server Error:", e)
        else:
            ExtractsCommand.exit_with_error(logger, "You must specify either a workbook or datasource")
