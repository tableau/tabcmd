from .global_options import *


class ListSitesParser:
    """
    Parser to list sites
    """

    @staticmethod
    def list_site_parser(manager, command):
        """Method to parse list sites arguments passed by the user"""
        list_site_parser = manager.include(command)
        set_view_site_encryption(list_site_parser)
