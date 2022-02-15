from .global_options import *


class CreateUserParser:
    """
    Parser for the command CreateUser
    """

    @staticmethod
    def create_user_parser(manager, command):
        """Method to parse create user arguments passed """
        create_users_parser = manager.include(command)
        set_users_file_positional(create_users_parser)
        set_role_arg(create_users_parser)
        set_no_wait_option(create_users_parser)
        set_completeness_options(create_users_parser)
        set_silent_option(create_users_parser)
