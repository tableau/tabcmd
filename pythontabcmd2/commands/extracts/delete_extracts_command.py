from .. import DeleteExtractsParser
import tableauserverclient as TSC
from .. import log
from ... import Session
from ..project.project_command import ProjectCommand
from ..extracts.extracts_command import ExtractsCommand


class DeleteExtracts(ExtractsCommand):
    """
    Command to delete extracts for a published workbook or data source.
    """
    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd2.deleteextracts_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args = DeleteExtractsParser.delete_extracts_parser()
        return cls(args)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.delete_extract(server_object)

    def delete_extract(self, server):
        if self.args.datasource:
            print(self.args.datasource)
            data_source_item = ExtractsCommand. \
                get_data_source_item(server, self.args.datasource)

            server.datasources.delete_extract(data_source_item)
        elif self.args.workbook:
            workbook_item = ExtractsCommand.get_workbook_item(server,
                                                              self.args
                                                              .workbook)
            server.workbooks.delete_extract(workbook_item)
