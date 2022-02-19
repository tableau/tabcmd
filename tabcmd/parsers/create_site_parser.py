from .global_options import *


class CreateSiteParser:
    """
    Parser for createsite command
    """

    @staticmethod
    def create_site_parser(manager, command):
        """Method to parse create site arguments passed by the user"""
        create_site_parser = manager.include(command)
        create_site_parser.add_argument('sitename', help='name of site')
        create_site_parser.add_argument('--url', '-r', default=None, help='used in URLs to specify site')
        set_site_args(create_site_parser)
