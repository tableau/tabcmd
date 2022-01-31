import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import RefreshExtractsParser


class RefreshExtracts:
    def __init__(self, args):
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd.refreshextract_command',
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
        pass
