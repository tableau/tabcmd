from .global_options import *


class DeleteSiteUsersParser:
    """
    Parser for the command deletesiteusers
    """

    @staticmethod
    def delete_site_users_parser(manager, command):
        """Method to parse delete site arguments passed by the user"""
        manager.include(command)
        delete_site_users_parser = manager.include(command)
        set_users_file_positional(delete_site_users_parser)
