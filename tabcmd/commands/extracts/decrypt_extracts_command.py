import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.extracts.extracts_command import ExtractsCommand
from tabcmd.execution.logger_config import log
from tabcmd.execution.localize import _


class DecryptExtracts(ExtractsCommand):
    """Command that decrypts all extracts on a site. If no site is
    specified, extracts on the default site will be decrypted."""

    name: str = "decryptextracts"
    description: str = _("decryptextracts.short_description")

    @staticmethod
    def define_args(decrypt_extract_parser):
        decrypt_extract_parser.add_argument("site_name", metavar="site-name", help=_("editsite.options.site-name"))

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        site_item = ExtractsCommand.get_site_for_command_or_throw(logger, server, args)
        try:
            ExtractsCommand.print_task_scheduling_message(logger, "site", site_item.name, "decrypted")
            job = server.sites.decrypt_extracts(site_item.id)
        except TSC.ServerResponseError as e:
            ExtractsCommand.exit_with_error(logger, "Error decrypting extracts", e)

        ExtractsCommand.print_success_message(logger, "decryption", job)
