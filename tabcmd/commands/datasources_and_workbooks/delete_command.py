import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import DeleteParser
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class DeleteCommand(DatasourcesAndWorkbooks):
    """
    Command to delete the specified workbook or data source from the server.
    """
    @classmethod
    def parse(cls):
        args = DeleteParser.delete_parser()
        return cls(args)

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        if args.workbook:
            # filter match the name and find id
            try:
                req_option = TSC.RequestOptions()
                req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                                 TSC.RequestOptions.
                                                 Operator.Equals,
                                                 args.workbook))
                matching_workbook, _ = server.workbooks.get(req_option)
                workbook_from_list = matching_workbook[0]
                server.workbooks.delete(workbook_from_list.id)
                logger.info("Workbook {} deleted".format(workbook_from_list.name))
            except IndexError:
                DeleteCommand.exit_with_error(logger, 'Workbook not found')
            except TSC.ServerResponseError as e:
                DeleteCommand.exit_with_error(logger, 'Server Error:', e)

        elif args.datasource:
            try:
                req_option = TSC.RequestOptions()
                req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                                 TSC.RequestOptions.
                                                 Operator.Equals,
                                                 args.datasource))
                matching_datasource, _ = server.workbooks.get(req_option)
                datasource_from_list = matching_datasource[0]
                server.datasources.delete(datasource_from_list.id)
            except IndexError:
                DeleteCommand.exit_with_error(logger, 'Datasource not found')
            except TSC.ServerResponseError as e:
                DeleteCommand.exit_with_error(logger, 'Server Error:', e)
        else:
            DeleteCommand.exit_with_error(logger, "You must specify either a workbook or datasource")
