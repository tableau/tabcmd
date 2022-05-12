import tableauserverclient as TSC

from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log
from tabcmd import _


class EditSiteCommand(Server):
    """
    Command to change the name of a site or its web folder name. Users can also use this command to allow or deny
    site administrators the ability to add and remove users, or prevent users from running certain tasks manually.
    """

    name: str = "editsite"
    description: str = _("editsite.short_description")

    @staticmethod
    def define_args(edit_site_parser):
        edit_site_parser.add_argument("site_name", metavar="site-name", help="name of site to update")
        edit_site_parser.add_argument(
            "--site-name", default=None, dest="new_site_name", help=_("editsite.options.site-name")
        )

        set_common_site_args(edit_site_parser)
        set_site_status_arg(edit_site_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)

        site_item = Server.get_site_for_command(logger, server, args, session)
        if args.url:
            site_item.content_url = args.url
        if args.user_quota:
            site_item.user_quota = args.user_quota
        if args.storage_quota:
            site_item.storage_quota = args.storage_quota
        if args.status:
            site_item.state = args.status
        try:
            server.sites.update(site_item)
            logger.info("Successfully updated the site `{}`".format(site_item.name))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Error editing site", e)
