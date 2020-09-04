import sys
from .parent_parser import ParentParser
from .common_parser import CommonParser


class CreateUserParser:
    """
    Parser for the command CreateUser
    """
    @staticmethod
    def create_user_parser():
        """Method to parse create user arguments passed """
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        create_users_parser = subparsers.add_parser('createusers',
                                                    parents=[parser])
        args = create_users_parser.parse_args(sys.argv[3:])
        csv_lines = CommonParser.read_file(sys.argv[2])
        if args.site is None or args.site == "Default":
            args.site = ''
        return csv_lines, args
