import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import CreateExtractsParser


class CreateExtracts:
    def __init__(self, args):
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('tabcmd.createextracts_command',
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
        pass
