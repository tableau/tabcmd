import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from ..auth.session import Session
from tabcmd.parsers.delete_parser import DeleteParser
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class DeleteCommand(DatasourcesAndWorkbooks):
    """
    Command to delete the specified workbook or data source from the server.
    """

    located_workbook = None
    located_datasource = None

    @classmethod
    def parse(cls):
        args = DeleteParser.delete_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        req_option = TSC.RequestOptions()
        possible_item = args.name or args.workbook or args.datasource
        try:
            req_option.filter.add(
                TSC.Filter(
                    TSC.RequestOptions.Field.Name,
                    TSC.RequestOptions.Operator.Equals,
                    possible_item,
                )
            )
            matching_workbook, _ = server.workbooks.get(req_option)
            matching_datasource, _ = server.datasources.get(req_option)
            if len(matching_workbook) == 1:  # found a matching workbook
                DeleteCommand.located_workbook = matching_workbook[0]
            elif len(matching_datasource) == 1:  # found a matching datasource
                DeleteCommand.located_datasource = matching_datasource[0]
            else:
                DeleteCommand.exit_with_error(logger, "No workbook or datasource found")
        except Exception as e:
            DeleteCommand.exit_with_error(logger, "Exception occurred", e)
        if args.workbook or DeleteCommand.located_workbook:
            # filter match the name and find id
            workbook_to_delete = DeleteCommand.located_workbook if DeleteCommand.located_workbook else args.workbook
            try:
                server.workbooks.delete(workbook_to_delete.id)
                logger.info("Workbook {} deleted".format(workbook_to_delete.name))
            except IndexError:
                DeleteCommand.exit_with_error(logger, "Workbook not found")
            except TSC.ServerResponseError as e:
                DeleteCommand.exit_with_error(logger, "Server Error:", e)

        elif args.datasource or DeleteCommand.located_datasource:
            datasource_to_delete = (
                DeleteCommand.located_datasource if DeleteCommand.located_datasource else args.datasource
            )
            logger.info("Workbook {} deleted".format(datasource_to_delete.name))
            try:
                server.datasources.delete(datasource_to_delete.id)
            except IndexError:
                DeleteCommand.exit_with_error(logger, "Datasource not found")
            except TSC.ServerResponseError as e:
                DeleteCommand.exit_with_error(logger, "Server Error:", e)
