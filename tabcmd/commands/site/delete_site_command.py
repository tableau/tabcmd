from .site_command import SiteCommand
import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from tabcmd.parsers.delete_site_parser import DeleteSiteParser
from ..auth.session import Session
from ..commands import Commands


class DeleteSiteCommand(SiteCommand):
    """
    Command to delete a site
    """

    @classmethod
    def parse(cls):
        args = DeleteSiteParser.delete_site_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        site_id = SiteCommand.find_site_id(server, args.site_name)
        try:
            server.sites.delete(site_id)
            logger.info("Successfully deleted the site")
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, "Server Error:", e)
