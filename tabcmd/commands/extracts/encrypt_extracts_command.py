from tabcmd.parsers.encrypt_extracts_parser import EncryptExtractsParser
import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from ..auth.session import Session
from ..extracts.extracts_command import ExtractsCommand
from ..site.site_command import SiteCommand


class EncryptExtracts(ExtractsCommand):
    """
    Command that encrypt all extracts on a site.
    If no site is specified, extracts on the default site will be encrypted.
    """

    @classmethod
    def parse(cls):
        args = EncryptExtractsParser.encrypt_extracts_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        try:
            site_id = SiteCommand.find_site_id(server, args.site_name)
            job = server.sites.encrypt_extracts(site_id)
            ExtractsCommand.print_success_message(logger, "encryption", job)
        except TSC.ServerResponseError as e:
            ExtractsCommand.exit_with_error(logger, "Server Error:", e)
