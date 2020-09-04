from .. import EncryptExtractsParser
import tableauserverclient as TSC
from .. import log
from ... import Session
from ..extracts.extracts_command import ExtractsCommand
from ..site.site_command import SiteCommand


class EncryptExtracts(ExtractsCommand):
    """
    Command that encrypt all extracts on a site.
    If no site is specified, extracts on the default site will be encrypted.
    """
    def __init__(self, args, site_name):
        super().__init__(args)
        self.site_name = site_name
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd2.encryptextracts_command',
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
        site_id = SiteCommand.find_site_id(server, self.site_name)
        server.sites.encrypt_extracts(site_id)
