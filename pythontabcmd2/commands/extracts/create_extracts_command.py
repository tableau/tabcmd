import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import CreateExtractsParser
from ..project.project_command import ProjectCommand
from ..extracts.extracts_command import ExtractsCommand


class CreateExtracts(ExtractsCommand):
    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd2.createextracts_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args = CreateExtractsParser.create_extracts_parser()
        return cls(args)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.create_extract(server_object)

    def create_extract(self, server):
        print(self.args)
        if self.args.datasource:

            data_source_item = ExtractsCommand.\
                get_data_source_item(server, self.args.datasource)

            server.datasources.create_extract(data_source_item,
                                              encrypt=self.args.encrypt)
        elif self.args.workbook:
            project_id = ProjectCommand.find_project_id(server,
                                                        self.args.project)
            workbook_item = ExtractsCommand.get_workbook_item(server,
                                                              self.args
                                                              .workbook)
            server.workbooks.create_extract(workbook_item,
                                            encrypt=self.args.encrypt,
                                            includeAll=self.args.include_all,
                                            datasources=self.args.embedded_datasources)
