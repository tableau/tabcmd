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
        target_site: TSC.SiteItem = Server.get_site_by_name(logger, server, args.site_name_to_delete)
        target_site_id = target_site.id
        logger.debug(strings[3].format(target_site_id, server.site_id))
        try:
            server.sites.delete(target_site_id)
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, strings[1], e)
        except Exception as e:
            Errors.exit_with_error(logger, strings[4], e)
        logger.info(strings[0].format(args.site_name_to_delete))


strings = [
    "Successfully deleted site {}",
    "Server responded with an error while deleting site",
    "name of site to delete",
    "Deleting site {0}, logged in to site {1}",
    "Error while deleting site",
]
