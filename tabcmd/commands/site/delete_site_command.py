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
        args_group = delete_site_parser.add_argument_group(title=DeleteSiteCommand.name)
        args_group.add_argument("site_name_to_delete", metavar="site-name", help=_("tabcmd.options.delete_site.name"))

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)
        target_site: TSC.SiteItem = Server.get_site_by_name(logger, server, args.site_name_to_delete)
        target_site_id = target_site.id
        logger.debug(_("tabcmd.deletesite.status_message").format(target_site_id, server.site_id))
        try:
            server.sites.delete(target_site_id)
            logger.info(_("tabcmd.deletesite.success").format(args.site_name_to_delete))
        except Exception as e:
            Errors.exit_with_error(logger, _("tabcmd.deletesite.error"), e)
