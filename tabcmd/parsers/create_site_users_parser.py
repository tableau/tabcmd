from .global_options import *


class CreateSiteUsersParser:
    """
    Parser for createsiteusers command
    """

    @staticmethod
    def create_site_user_parser(manager, command):
        """Method to parse create site users arguments passed by the user"""

        create_site_users_parser = manager.include(command)
        set_role_arg(create_site_users_parser)
        set_users_file_positional(create_site_users_parser)

