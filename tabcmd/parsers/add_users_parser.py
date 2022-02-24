from .global_options import *


class AddUserParser:
    """
    Parser for AddUser command
    """

    @staticmethod
    def add_user_parser(manager, command):
        """Method to parse add user arguments passed"""

        add_user_parser = manager.include(command)
        add_user_parser.add_argument("name", help="name of group to add users to")
        set_users_file_arg(add_user_parser)
        set_completeness_options(add_user_parser)
