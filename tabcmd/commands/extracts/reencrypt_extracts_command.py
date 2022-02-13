from .. import ReencryptExtractsParser
import tableauserverclient as TSC
from .. import log
from ... import Session
from ..extracts.extracts_command import ExtractsCommand
from ..site.site_command import SiteCommand


class ReencryptExtracts(ExtractsCommand):
    """
    Command to Reencrypt all extracts on a site with new encryption keys.
    This command will regenerate the key encryption key and data encryption key. You must specify a site.
    """
    @classmethod
    def parse(cls):
        args = ReencryptExtractsParser.reencrypt_extracts_parser()
        return cls(args)

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        try:
            site_id = SiteCommand.find_site_id(server, args.site_name)
            job = server.sites.encrypt_extracts(site_id)
            ExtractsCommand.print_success_message(logger, 're-encryption', job)
        except TSC.ServerResponseError as e:
            ExtractsCommand.exit_with_error(logger, 'Server Error', e)
