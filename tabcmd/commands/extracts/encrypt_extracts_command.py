import tableauserverclient as TSC
from .. import log
from ... import Session
from .. import EncryptExtractsParser


class EncryptExtracts:
    def __init__(self, args, site_name):
        self.site_name = site_name
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('tabcmd.encryptextracts_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args, site_name = EncryptExtractsParser.encrypt_extracts_parser()
        return cls(args, site_name)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.encrypt_extract(server_object)

    def encrypt_extract(self, server):
        pass
