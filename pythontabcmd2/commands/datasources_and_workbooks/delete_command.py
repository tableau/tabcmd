import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import DeleteParser


class DeleteCommand:
    def __init__(self, args):
        self.workbook = args.workbook
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd2.delete_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args = DeleteParser.delete_parser()
        return cls(args)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.delete(server_object)

    def delete(self, server):
        """Method to delete datasources_and_workbooks using
        Tableauserverclient methods"""
        if self.workbook:
            # filter match the name and find id
            try:
                req_option = TSC.RequestOptions()
                req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                                 TSC.RequestOptions.
                                                 Operator.Equals,
                                                 self.workbook))
                matching_workbook, _ = server.workbooks.get(
                    req_option)
                workbook_from_list = matching_workbook[0]
                server.workbooks.delete(workbook_from_list.id)
                self.logger.info("Workbook {} deleted".format(
                    workbook_from_list.name))
            except IndexError:
                self.logger.error("Please check if workbook is present")
            except TSC.ServerResponseError as e:
                self.logger.error("Server error occurred")

        if self.args.datasource:
            try:
                req_option = TSC.RequestOptions()
                req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                                 TSC.RequestOptions.
                                                 Operator.Equals,
                                                 self.args.datasource))
                matching_datasource, _ = server.workbooks.get(
                    req_option)
                datasource_from_list = matching_datasource[0]
                server.datasources.delete(datasource_from_list.id)
            except IndexError:
                self.logger.error("Please check if data source is present")
            except TSC.ServerResponseError as e:
                self.logger.error("Server error occurred")
