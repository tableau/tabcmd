import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class CreateSiteCommand(Server):
    """
    Command to Create a site
    """

    name: str = "createsite"
    description: str = _("createsite.short_description")

    @staticmethod
    def define_args(create_site_parser):
        args_group = create_site_parser.add_argument_group(title=CreateSiteCommand.name)
        args_group.add_argument("new_site_name", metavar="site-name", help=_("editsite.options.site-name"))
        set_common_site_args(args_group)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug("======================== {} {} =======================".format("tabcmd", __class__.name))
        session = Session()
        server = session.create_session(args, logger)
        admin_mode = "ContentAndUsers"  # default: allow site admins to manage users
        if not args.site_admin_user_management:
            admin_mode = "ContentOnly"
        new_site = TSC.SiteItem(
            name=args.new_site_name,
            content_url=args.url or args.new_site_name,
            admin_mode=admin_mode,
            user_quota=args.user_quota,
            storage_quota=args.storage_quota,
        )
        try:
            logger.info(_("createsite.status").format(args.new_site_name))
            server.sites.create(new_site)
            logger.info(_("common.output.succeeded"))
        except Exception as e:
            if Errors.is_resource_conflict(e) and args.continue_if_exists:
                logger.info(_("createsite.errors.site_name_already_exists").format(args.new_site_name))
                return
            Errors.exit_with_error(logger, e)
