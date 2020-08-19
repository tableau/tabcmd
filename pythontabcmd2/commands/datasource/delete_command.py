
import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import DeleteDataSourceParser


class DeleteDataSource:
    def __init__(self, args):
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd2.delete_data_source_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args = DeleteDataSourceParser.delete_data_source_parser()
        return cls(args)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.delete_data_source(server_object)

    def delete_data_source(self, server):
        """Method to delete datasource using Tableauserverclient methods"""
        if self.args.workbook:
            # filter match the name and find id
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                             TSC.RequestOptions.Operator.Equals,
                                             self.args.workbook))
            matching_workbook, _ = server.workbooks.get(
                req_option)
            workbook_from_list = matching_workbook[0]
            server.workbooks.delete(workbook_from_list.id)



        # try:
        #     group_id = GroupCommand.find_group_id(server, self.name)
        #     server.groups.delete(group_id)
        #     self.logger.info("Successfully deleted group")
        # except TSC.ServerResponseError as e:
        #     self.logger.error("Server error occurred", e)
        #
