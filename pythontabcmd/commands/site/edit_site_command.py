from logging import Logger

import tableauserverclient as TSC
from .. import log
from ...parsers.edit_site_parser import EditSiteParser
from .site_command import SiteCommand
from ... import Session


class EditSiteCommand(SiteCommand):
    """
    Command to change the name of a site or its web folder name.
    Users can also use this command to allow or deny site administrators
    the ability to add and remove users, or prevent users from
    running certain tasks manually.
    """

    def __init__(self, args, admin_mode, current_site_id):
        super().__init__(args)
        self.current_site = current_site_id
        self.site_id = args.site_id
        self.site_name = args.site_name
        self.admin_mode = admin_mode
        self.status = args.status
        self.url = args.url
        self.extract_encryption_mode = args.extract_encryption_mode
        self.run_now_enabled = args.run_now_enabled
        self.user_quota = args.user_quota
        self.storage_quota = args.storage_quota
        self.logger = log('pythontabcmd.edit_site_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args, admin_mode, current_site_id = EditSiteParser.edit_site_parser()
        return cls(args, admin_mode, current_site_id)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.edit_site(server_object)

    def edit_site(self, server):
        """Method to edit a site using tableauserverclient methods"""
        site_item = self.get_site(server, self.current_site)
        if self.url is not None:
            site_item.content_url = self.url
        if self.site_name is not None:
            site_item.name = self.site_name
        if self.site_id is not None:
            site_item.id = self.site_id
        if self.user_quota is not None:
            site_item.user_quota = self.user_quota
        if self.storage_quota is not None:
            site_item.storage_quota = self.storage_quota
        if self.status is not None:
            site_item.state = self.status
        self.edit_site_helper(server, site_item)

    def edit_site_helper(self, server, site):
        """ Helper method to catch server errors
        thrown by tableauserverclient"""
        try:
            server.sites.update(site)
            self.logger.info('Successfully updated the site called: {'
                             '}'.format(site.name))
        except TSC.ServerResponseError as e:
            self.logger.error('error updating the site', e)

    def get_site(self, server, current_site):
        site_item = None
        all_sites, pagination_item = server.sites.get()
        for site in all_sites:
            if site.content_url == current_site:
                site_item = site
                break
        return site_item
