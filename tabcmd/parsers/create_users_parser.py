import sys
from .parent_parser import ParentParser
from .common_parser import CommonParser


class CreateUserParser:
    """
    Parser for the command CreateUser
    """
    USER_ARG_IDX = 3
    USER_ARG_FILE_NAME_IDX = 2

    @staticmethod
    def create_user_parser():
        """Method to parse create user arguments passed """
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        create_users_parser = subparsers.add_parser('createusers',
                                                    parents=[parser])
        args = create_users_parser.parse_args(sys.argv[CreateUserParser.
                                              USER_ARG_IDX:])
        csv_lines = CommonParser.read_file(sys.argv[CreateUserParser.
                                           USER_ARG_FILE_NAME_IDX])
        if args.site is None or args.site == "Default":
            args.site = ''
        return csv_lines, args
