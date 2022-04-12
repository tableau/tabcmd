import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log


class DeleteSiteCommand(Server):
    """
    Command to delete a site
    """

    name: str = "deletesite"
    description: str = "Delete a site"

    @staticmethod
    def define_args(delete_site_parser):
        delete_site_parser.add_argument("site_name", help="name of site to delete")

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        site_id = server.sites.get_by_name(args.site_name)
        if site_id == session.site_id:
            Errors.exit_with_error(logger, "Cannot delete the site you are logged in to")
        try:
            server.sites.delete(site_id)
            logger.info("Successfully deleted the site")
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Error deleting site", e)
