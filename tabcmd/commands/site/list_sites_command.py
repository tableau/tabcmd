import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from tabcmd.parsers.list_sites_parser import ListSitesParser
from ..commands import Commands
from .site_command import SiteCommand
from ..auth.session import Session


class ListSiteCommand(SiteCommand):
    """
    Command to return a list of sites to which the logged in user belongs
    """

    @classmethod
    def parse(cls):
        args = ListSitesParser.list_site_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        try:
            # TODO should wrap this in Commands so we always handle the server the same
            # TODO we need to implement paging
            # TODO should say `Listing sites for username`
            all_sites, pagination_item = server.sites.get()
            logger.info("===== Listing sites...")
            for site in all_sites:
                print("NAME:", site.name)
                print("SITEID:", site.content_url)
                if args.get_extract_encryption_mode:
                    print("EXTRACTENCRYPTION:", site.extract_encryption_mode)
                print("")
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, e)
