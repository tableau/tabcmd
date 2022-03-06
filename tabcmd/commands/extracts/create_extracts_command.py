import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.extracts.extracts_command import ExtractsCommand
from tabcmd.execution.logger_config import log


class CreateExtracts(ExtractsCommand):
    """
    Command that creates extracts for a published workbook or data source.
    """

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
                data_source_item = ExtractsCommand.get_data_source_item(server, args.datasource)
                job = server.datasources.create_extract(data_source_item, encrypt=args.encrypt)

            elif args.workbook:
                logger.debug("Finding workbook `{}` on the server...".format(args.workbook))
                ExtractsCommand.print_task_scheduling_message(logger, "workbook", args.workbook, "created")
                workbook_item = ExtractsCommand.get_workbook_item(server, args.workbook)
                job = server.workbooks.create_extract(
                    workbook_item,
                    encrypt=args.encrypt,
                    includeAll=args.include_all,
                    datasources=args.embedded_datasources,
                )
        except TSC.ServerResponseError as e:
            ExtractsCommand.exit_with_error(logger, "Error creating extracts", e)

        ExtractsCommand.print_success_message(logger, "creation", job)
