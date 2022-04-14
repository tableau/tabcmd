import tableauserverclient as TSC

from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log


class CreateSiteCommand(Server):
    """
    Command to Create a site
    """

    name: str = "createsite"
    description: str = "Create a site"

    @staticmethod
    def define_args(create_site_parser):
        create_site_parser.add_argument("site_name", metavar="site-name", help="name of site")
        set_common_site_args(create_site_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
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
            server.sites.create(new_site)
            logger.info("Successfully created a new site called: {}".format(args.site_name))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "error creating site", e)
