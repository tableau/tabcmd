from .global_options import *


class RemoveUserParser:
    """
    Parser to removeusers command
    """

    @staticmethod
    def remove_user_parser(manager, command):
        """Method to parse remove user arguments passed by the user"""
        remove_users_parser = manager.include(command)
        remove_users_parser.add_argument('groupname',
                                         help='The group to remove users from.')
        set_users_file_arg(remove_users_parser)
        set_completeness_options(remove_users_parser)
