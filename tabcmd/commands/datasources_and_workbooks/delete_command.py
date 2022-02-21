import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from ..auth.session import Session
from tabcmd.parsers.delete_parser import DeleteParser
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class DeleteCommand(DatasourcesAndWorkbooks):
    """
    Command to delete the specified workbook or data source from the server.
    """

    @classmethod
    def parse(cls):
        args = DeleteParser.delete_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        located_workbook = None
        located_datasource = None
        req_option = TSC.RequestOptions()
        possible_workbook = args.name if args.name else args.workbook
        possible_datasource = args.name if args.name else args.datasource
        try:
            req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                             TSC.RequestOptions.
                                             Operator.Equals,
                                             possible_workbook))
            matching_workbook, _ = server.workbooks.get(req_option)
            located_workbook = matching_workbook[0]

        except IndexError:  # did not find a workbook so try if there is a datasource with that name
            try:
                req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                                 TSC.RequestOptions.
                                                 Operator.Equals,
                                                 possible_datasource))
                matching_datasource, _ = server.workbooks.get(req_option)
                located_datasource = matching_datasource[0]
            except IndexError:
                DeleteCommand.exit_with_error(logger, 'No workbook or datasource found')

        if args.workbook or located_workbook:
            # filter match the name and find id
            workbook_to_delete = located_workbook if located_workbook else args.workbook
            try:
                server.workbooks.delete(workbook_to_delete.id)
                logger.info("Workbook {} deleted".format(workbook_to_delete.name))
            except IndexError:
                DeleteCommand.exit_with_error(logger, 'Workbook not found')
            except TSC.ServerResponseError as e:
                DeleteCommand.exit_with_error(logger, 'Server Error:', e)

        elif args.datasource or located_datasource:
            datasource_to_delete = located_datasource if located_datasource else args.datasource
            try:
                server.datasources.delete(datasource_to_delete.id)
            except IndexError:
                DeleteCommand.exit_with_error(logger, 'Datasource not found')
            except TSC.ServerResponseError as e:
                DeleteCommand.exit_with_error(logger, 'Server Error:', e)
        else:
            DeleteCommand.exit_with_error(logger, "You must specify either a workbook or datasource")
