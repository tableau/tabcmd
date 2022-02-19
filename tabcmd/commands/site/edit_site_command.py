import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from tabcmd.parsers.edit_site_parser import EditSiteParser
from .site_command import SiteCommand
from ..auth.session import Session
from ..commands import Commands


class EditSiteCommand(SiteCommand):
    """
    Command to change the name of a site or its web folder name. Users can also use this command to allow or deny
    site administrators the ability to add and remove users, or prevent users from running certain tasks manually.
    """
    @classmethod
    def parse(cls):
        args = EditSiteParser.edit_site_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        site_item = EditSiteCommand.get_site(server, args.site_name)
        if site_item is None:
            SiteCommand.exit_with_error(logger, 'Site not found')
        if args.url is not None:
            site_item.content_url = args.url
        if args.site_name is not None:
            site_item.name = args.site_name
        if args.site_id is not None:
            site_item.id = args.site_id
        if args.user_quota is not None:
            site_item.user_quota = args.user_quota
        if args.storage_quota is not None:
            site_item.storage_quota = args.storage_quota
        if args.status is not None:
            site_item.state = args.status
        try:
            server.sites.update(site_item)
            logger.info('Successfully updated the site called: {}'.format(args.site_name))
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, 'error updating the site', e)

    @staticmethod
    def get_site(server, site_to_find):
        site_item = None
        all_sites, pagination_item = server.sites.get()
        for site in all_sites:
            if site.content_url == site_to_find:
                site_item = site
                break
        return site_item
