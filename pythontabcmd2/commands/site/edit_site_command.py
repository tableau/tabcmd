import tableauserverclient as TSC
from .. import log
from ...parsers.edit_site_parser import EditSiteParser
from .site_command import SiteCommand
from ... import Session


class EditSiteCommand(SiteCommand):
    def __init__(self, args, admin_mode):
        super().__init__(args)
        self.site_name = args.site_name
        self.site_id = args.site_id
        self.admin_mode = admin_mode
        self.status = args.status
        self.extract_encryption_mode = args.extract_encryption_mode
        self.run_now_enabled = args.run_now_enabled
        self.user_quota = args.user_quota
        self.storage_quota = args.storage_quota
        self.logger = log('pythontabcmd2.edit_site_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args, admin_mode = EditSiteParser.edit_site_parser()
        return cls(args, admin_mode)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.edit_site(server_object)

    def edit_site(self, server):
        """Method to edit a site using tableauserverclient methods"""
        new_site = TSC.SiteItem(name=self.site_name, admin_mode=self.admin_mode,
                                user_quota=self.user_quota,   # TODO: ASK
                                storage_quota=self.storage_quota)
        self.edit_site_helper(server, new_site)

    def edit_site_helper(self, server, site):
        """ Helper method to catch server errors
        thrown by tableauserverclient"""
        try:
            server.sites.update(site)
            self.logger.info('Successfully updated the site called:')
        except TSC.ServerResponseError as e:
            self.logger.error('error updating the site')
