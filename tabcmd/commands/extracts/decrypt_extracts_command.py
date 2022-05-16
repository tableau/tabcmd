import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.extracts.extracts_command import ExtractsCommand
from tabcmd.execution.logger_config import log
from tabcmd import _


class DecryptExtracts(ExtractsCommand):
    """Command that decrypts all extracts on a site. If no site is
    specified, extracts on the default site will be decrypted."""

    name: str = "decryptextracts"
    description: str = _("decryptextracts.short_description")

    @staticmethod
    def define_args(decrypt_extract_parser):
        # TODO this argument is supposed to be optional - if not specified, do the default site
        decrypt_extract_parser.add_argument("site_name", metavar="site-name", help="name of site")

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        site_item = ExtractsCommand.get_site_for_command(logger, server, args, session)
        try:
            ExtractsCommand.print_task_scheduling_message(logger, "site", site_item.name, "decrypted")
            job = server.sites.decrypt_extracts(site_item.id)
        except TSC.ServerResponseError as e:
            ExtractsCommand.exit_with_error(logger, "Error decrypting extracts", e)

        ExtractsCommand.print_success_message(logger, "decryption", job)
