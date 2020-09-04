import tableauserverclient as TSC
from .. import log
from ...parsers.create_site_parser import CreateSiteParser
from .site_command import SiteCommand
from ... import Session


class CreateSiteCommand(SiteCommand):
    """
    Command to Create a site
    """
    def __init__(self, args, admin_mode):
        super().__init__(args)
        self.site_name = args.site_name
        self.admin_mode = admin_mode
        self.url = args.url
        self.user_quota = args.user_quota
        self.storage_quota = args.storage_quota
        self.logger = log('pythontabcmd2.create_site_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args, admin_mode = CreateSiteParser.create_site_parser()
        return cls(args, admin_mode)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.create_site(server_object)

    def create_site(self, server):
        """Method to create a site using tableauserverclient methods"""
        new_site = TSC.SiteItem(name=self.site_name, content_url=self.url,
                                admin_mode=self.admin_mode,
                                user_quota=self.user_quota,
                                storage_quota=self.storage_quota)
        self.create_site_helper(server, new_site)

    def create_site_helper(self, server, site):
        """ Helper method to catch server errors
        thrown by tableauserverclient"""
        try:
            server.sites.create(site)
            self.logger.info("Successfully created a new site called: {}"
                             "".format(self.site_name))
        except TSC.ServerResponseError as e:
            self.logger.error('error creating site', e)
