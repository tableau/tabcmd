import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.extracts.extracts_command import ExtractsCommand
from tabcmd.commands.site.site_command import SiteCommand
from tabcmd.execution.logger_config import log


class ReencryptExtracts(ExtractsCommand):
    """
    Command to Reencrypt all extracts on a site with new encryption keys.
    This command will regenerate the key encryption key and data encryption key. You must specify a site.
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        site_item = ExtractsCommand.get_site_for_command(logger, server, args, session)
        try:
            ExtractsCommand.print_task_scheduling_message(logger, "site", site_item.name, "re-encrypted")
            job = server.sites.encrypt_extracts(site_item.id)
        except TSC.ServerResponseError as e:
            ExtractsCommand.exit_with_error(logger, "Error re-encrypting extract", e)
        ExtractsCommand.print_success_message(logger, "re-encryption", job)
