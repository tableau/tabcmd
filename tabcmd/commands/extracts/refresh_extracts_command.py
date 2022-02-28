from tabcmd.parsers.refresh_extracts_parser import RefreshExtractsParser
import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from ..auth.session import Session
from ..extracts.extracts_command import ExtractsCommand


class RefreshExtracts(ExtractsCommand):
    """
    Command to Perform a full or incremental refresh of extracts belonging to the specified workbook or data source.
    """

    @classmethod
    def parse(cls):
        args = RefreshExtractsParser.refresh_extracts_parser()
        return args

    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        if args.datasource:
            try:
                datasource_id = ExtractsCommand.get_data_source_id(
                    server, args.datasource
                )
                job = server.datasources.refresh(datasource_id)
                ExtractsCommand.print_success_message(logger, "refresh", job)
            except TSC.ServerResponseError as e:
                ExtractsCommand.exit_with_error(logger, "Server Error", e)

        elif args.workbook:
            try:
                workbook_id = ExtractsCommand.get_workbook_id(server, args.workbook)
                job = server.workbooks.refresh(workbook_id)
                ExtractsCommand.print_success_message(logger, "refresh", job)
            except TSC.ServerResponseError as e:
                ExtractsCommand.exit_with_error(logger, "Server Error", e)
        else:
            ExtractsCommand.exit_with_error(
                logger, "You must specify either a workbook or datasource"
            )
