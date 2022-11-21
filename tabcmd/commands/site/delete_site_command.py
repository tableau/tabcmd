import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class DeleteSiteCommand(Server):
    """
    Command to delete a site
    """

    name: str = "deletesite"
    description: str = _("deletesite.short_description")

    @staticmethod
    def define_args(delete_site_parser):
        delete_site_parser.add_argument("site_name_to_delete", metavar="site-name", help=strings[2])

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        site_url = Server.get_site_by_name(logger, server, args.site_name_to_delete).content_url
        logger.debug(strings[3].format(site_url))
        try:
            server.sites.delete(site_url)
            logger.info(strings[0])
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, strings[1], e)
        except BaseException as e:
            Errors.exit_with_error(logger, strings[4], e)


strings = [
    "Successfully deleted the site",
    "Server responded with an error while deleting site",
    "name of site to delete",
    "Deleting site  {}",
    "Error while deleting site",
]
