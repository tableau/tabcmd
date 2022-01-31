import tableauserverclient as TSC
from .. import log
from ...parsers.list_sites_parser import ListSitesParser
from .site_command import SiteCommand
from ... import Session


class ListSiteCommand(SiteCommand):
    """
    Command to return a list of sites to which the logged in user belongs
    """
    def __init__(self, args):
        super().__init__(args)
        self.logger = log('pythontabcmd.list_sites_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args = ListSitesParser.list_site_parser()
        return cls(args)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.list_sites(server_object)

    def list_sites(self, server):
        """Method to list sites using tableauserverclient methods"""
        try:
            all_sites, pagination_item = server.sites.get()
            for site in all_sites:
                print(site.id, site.name, site.content_url, site.state)
        except TSC.ServerResponseError as e:
            self.logger.error('error getting all sites', e)
