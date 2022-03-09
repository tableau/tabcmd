from .global_options import *


class CreateSiteParser:
    """
    Parser for createsite command
    """

    @staticmethod
    def create_site_parser(manager, command):
        """Method to parse create site arguments passed by the user"""
        create_site_parser = manager.include(command)
        create_site_parser.add_argument("site_name", metavar="site-name", help="name of site")
        set_common_site_args(create_site_parser)
