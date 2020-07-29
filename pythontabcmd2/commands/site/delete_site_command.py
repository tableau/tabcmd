from .site_command import SiteCommand
from .. import CreateProjectParser
from ..commands import Commands
import tableauserverclient as TSC
from .. import get_logger
from ...parsers.delete_site_parser import DeleteSiteParser

logger = get_logger('pythontabcmd2.delete_site_command')


class DeleteSiteCommand:
    def __init__(self, args):
        self.site_name = args.site_name

    @classmethod
    def parse(cls):
        args = DeleteSiteParser.delete_site_parser()
        return cls(args)

    def run_command(self):
        signed_in_object, server_object = Commands.deserialize()
        self.delete_site(server_object, self.site_name)

    def delete_site(self, server, site_name):
        """Method to delete a site using tableauserverclient methods"""
        self.delete_site_helper(server, site_name)

    def create_site_helper(self, server, site_name):
        """ Helper method to catch server errors thrown
        by tableauserverclient"""
        site_id = SiteCommand.find_site_id()
        try:
            server.sites.delete(site_id)
            logger.info('Successfully deletes the site')
        except TSC.ServerResponseError as e:
            print(e)
