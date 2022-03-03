import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.commands import Commands
from tabcmd.execution.logger_config import log
from .site_command import SiteCommand


class ListSiteCommand(SiteCommand):
    """
    Command to return a list of sites to which the logged in user belongs
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        try:
            all_sites, pagination_item = server.sites.get()
            for site in all_sites:
                print(site.id, site.name, site.content_url, site.state)
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, "error getting all sites", e)
