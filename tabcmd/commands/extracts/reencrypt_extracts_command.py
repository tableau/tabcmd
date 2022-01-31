import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import ReencryptExtractsParser


class ReencryptExtracts:
    def __init__(self, args, site_name):
        self.site_name = site_name
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('tabcmd.reencryptextracts_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args, site_name = ReencryptExtractsParser.reencrypt_extracts_parser()
        return cls(args, site_name)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.reencrypt_extract(server_object)

    def reencrypt_extract(self, server):
        pass
