import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.extracts.extracts_command import ExtractsCommand
from tabcmd.execution.logger_config import log


class EncryptExtracts(ExtractsCommand):
    """
    Command that encrypt all extracts on a site.
    If no site is specified, extracts on the default site will be encrypted.
    """

    name: str = "encryptextracts"
    description: str = "Encrypt extracts on a site"

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        site_item = ExtractsCommand.get_site_for_command(logger, server, args, session)
        try:
            ExtractsCommand.print_task_scheduling_message(logger, "site", site_item.name, "encrypted")
            job = server.sites.encrypt_extracts(site_item.id)
        except TSC.ServerResponseError as e:
            ExtractsCommand.exit_with_error(logger, "Error encrypting extracts", e)

        ExtractsCommand.print_success_message(logger, "encryption", job)
