import tableauserverclient as TSC

from src.commands.auth.session import Session
from src.commands.constants import Errors
from src.commands.server import Server
from src.execution.global_options import *
from src.execution.localize import _
from src.execution.logger_config import log


class CreateSiteCommand(Server):
    """
    Command to Create a site
    """

    name: str = "createsite"
    description: str = _("createsite.short_description")

    @staticmethod
    def define_args(create_site_parser):
        create_site_parser.add_argument("site_name", metavar="site-name", help=_("editsite.options.site-name"))
        set_common_site_args(create_site_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        new_site = TSC.SiteItem(
            name=args.site_name,
            content_url=args.url,
            admin_mode=args.admin_mode,
            user_quota=args.user_quota,
            storage_quota=args.storage_quota,
        )
        try:
            logger.info(_("createsite.status").format(args.site_name))
            server.sites.create(new_site)
            logger.info(_("common.output.succeeded"))
        except TSC.ServerResponseError as e:
            if Errors.is_resource_conflict(e):
                if args.continue_if_exists:
                    logger.info(_("createsite.errors.site_name_already_exists").format(args.site_name))
                    return
                else:
                    Errors.exit_with_error(
                        logger, _("createsite.errors.site_name_already_exists").format(args.site_name)
                    )

            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response"), e)
