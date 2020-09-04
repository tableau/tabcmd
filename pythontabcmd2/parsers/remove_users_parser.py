import argparse
import sys
from .parent_parser import ParentParser
from .common_parser import CommonParser


class RemoveUserParser:
    """
    Parser to removeusers command
    """
    @staticmethod
    def remove_user_parser():
        """Method to parse remove user arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        remove_users_parser = subparsers.add_parser('removeusers',
                                                    parents=[parser])

        remove_users_parser.add_argument('--users', required=True,
                                         help='csv containing user details')
        args = remove_users_parser.parse_args(sys.argv[3:])
        group_name = sys.argv[2]
        csv_lines = CommonParser.read_file(args.users)
        if args.site is None or args.site == "Default":
            args.site = ''
        return csv_lines, args, group_name

# TODO: ARGUMENT --COMPLETE
