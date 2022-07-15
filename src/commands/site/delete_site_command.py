import tableauserverclient as TSC

from src.commands.auth.session import Session
from src.commands.constants import Errors
from src.commands.server import Server
from src.execution.localize import _
from src.execution.logger_config import log


class DeleteSiteCommand(Server):
    """
    Command to delete a site
    """

    name: str = "deletesite"
    description: str = _("deletesite.short_description")

    @staticmethod
    def define_args(delete_site_parser):
        delete_site_parser.add_argument("site_name_to_delete", metavar="site-name", help="name of site to delete")

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        site_url = Server.get_site_by_name(logger, server, args.site_name_to_delete).content_url
        try:
            server.sites.delete(site_url)
            logger.info("Successfully deleted the site")
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Error deleting site", e)
