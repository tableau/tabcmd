import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import DeleteExtractsParser


class DeleteExtracts:
    def __init__(self, args):
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd.deleteextracts_command',
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
        pass
