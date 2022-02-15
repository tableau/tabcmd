from .global_options import *


class DeleteSiteParser:
    """
    Parser for the command deletesite
    """

    @staticmethod
    def delete_site_parser(manager, command):
        """Method to parse delete site arguments passed by the user"""
        delete_site_parser = manager.include(command)
        delete_site_parser.add_argument('sitename', help='name of site to delete')

