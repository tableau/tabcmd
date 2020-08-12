from .site_command import SiteCommand
from ..commands import Commands
import tableauserverclient as TSC
from .. import log
from ...parsers.delete_site_parser import DeleteSiteParser
from ... import Session


class DeleteSiteCommand(SiteCommand):
    def __init__(self, args):
        super().__init__(args)
        self.site_name = args.site_name
        self.logger = log('pythontabcmd2.delete_site_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args = DeleteSiteParser.delete_site_parser()
        return cls(args)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.delete_site(server_object, self.site_name)

    def delete_site(self, server, site_name):
        """Method to delete a site using tableauserverclient methods"""
        self.delete_site_helper(server, site_name)

    def delete_site_helper(self, server, site_name):
        """ Helper method to catch server errors thrown
        by tableauserverclient"""
        site_id = SiteCommand.find_site_id(server, self.args.site_name)
        try:
            server.sites.delete(site_id)
            self.logger.info('Successfully deleted the site')
        except TSC.ServerResponseError as e:
            print(e)
