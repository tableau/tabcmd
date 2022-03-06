import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.commands import Commands
from tabcmd.execution.logger_config import log
from .site_command import SiteCommand


class DeleteSiteCommand(SiteCommand):
    """
    Command to delete a site
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        site_id = server.sites.get_by_name(args.site_name)
        if site_id == session.site_id:
            Commands.exit_with_error(logger, "Cannot delete the site you are logged in to")
        try:
            server.sites.delete(site_id)
            logger.info("Successfully deleted the site")
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, "Error deleting site", e)
