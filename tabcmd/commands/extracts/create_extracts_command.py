import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from ..auth.session import Session
from tabcmd.parsers.create_extracts_parser import CreateExtractsParser
from ..project.project_command import ProjectCommand
from ..extracts.extracts_command import ExtractsCommand


class CreateExtracts(ExtractsCommand):
    """
    Command that creates extracts for a published workbook or data source.
    """

    @classmethod
    def parse(cls):
        args = CreateExtractsParser.create_extracts_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        if args.datasource:
            try:
                data_source_item = ExtractsCommand.get_data_source_item(server, args.datasource)
                job = server.datasources.create_extract(data_source_item, encrypt=args.encrypt)
                ExtractsCommand.print_success_message(logger, 'creation', job)
            except TSC.ServerResponseError as e:
                ExtractsCommand.exit_with_error(logger, "Server Error:", e)
        elif args.workbook:
            try:
                # this isn't used anywhere?
                project_id = ProjectCommand.find_project_id(server, args.project)
                workbook_item = ExtractsCommand.get_workbook_item(server, args.workbook)
                job = server.workbooks.create_extract(workbook_item,
                                                      encrypt=args.encrypt,
                                                      includeAll=args.include_all,
                                                      datasources=args.embedded_datasources)
                ExtractsCommand.print_success_message(logger, 'creation', job)
            except TSC.ServerResponseError as e:
                ExtractsCommand.exit_with_error(logger, "Server Error:", e)
        else:
            ExtractsCommand.exit_with_error(logger, "You must specify either a workbook or datasource")
