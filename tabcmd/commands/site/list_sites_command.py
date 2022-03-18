import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log
from .site_command import SiteCommand


class ListSiteCommand(SiteCommand):
    """
    Command to return a list of sites to which the logged in user belongs
    """

    name: str = "listsites"
    description: str = "List sites for user"

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        try:
            sites = ListSiteCommand.get_sites(server)
            logger.info("===== Listing sites for user {}...".format(session.username))
            for site in sites:
                print("NAME:", site.name)
                print("SITEID:", site.content_url)
                if args.get_extract_encryption_mode:
                    print("EXTRACTENCRYPTION:", site.extract_encryption_mode)
                print("")
        except TSC.ServerResponseError as e:
            Server.exit_with_error(logger, e)
