import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import RefreshExtractsParser
from ..extracts.extracts_command import ExtractsCommand
from ..site.site_command import SiteCommand


class RefreshExtracts(ExtractsCommand):
    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd2.refreshextract_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args = RefreshExtractsParser.refresh_extracts_parser()
        return cls(args)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.refresh_extracts(server_object)

    def refresh_extracts(self, server):
        if self.args.datasource:
            datasource_id = ExtractsCommand.get_data_source_id(
                server, self.args.datasource)

            server.datasources.refresh(datasource_id)
        elif self.args.workbook:
            workbook_id = ExtractsCommand.get_workbook_id(server,
                                                          self.args.workbook)

            server.workbooks.refresh(workbook_id)
