import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class ListSiteCommand(Server):
    """
    Command to return a list of sites to which the logged in user belongs
    """

    name: str = "listsites"
    description: str = _("listsites.short_description")

    @staticmethod
    def define_args(list_site_parser):
        group = list_site_parser.add_argument_group(title=ListSiteCommand.name)
        set_site_detail_option(group)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)
        try:
            sites, pagination = server.sites.get()
            logger.info(_("listsites.status").format(session.username))
            for site in sites:
                logger.info(_("listsites.output").format(" ", site.name, site.id))
                if args.get_extract_encryption_mode:
                    logger.info("EXTRACTENCRYPTION: {}".format(site.extract_encryption_mode))
        except Exception as e:
            Errors.exit_with_error(logger, e)
