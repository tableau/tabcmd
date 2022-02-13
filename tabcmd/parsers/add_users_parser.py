import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser
from .common_parser import CommonParser


class AddUserParser:
    """
    Parser for AddUser command
    """
    USER_ARG_IDX = 3
    USER_GROUP_ARG_IDX = 2

    @staticmethod
    def add_user_parser():
        """Method to parse add user arguments passed """
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        add_user_parser = subparsers.add_parser('adduser', parents=[parser])
        add_user_parser.add_argument('--users', required=True, help='csv containing user details')
        args = add_user_parser.parse_args(sys.argv[AddUserParser.USER_ARG_IDX:])
        args.group_name = sys.argv[AddUserParser.USER_GROUP_ARG_IDX]
        args.csv_lines = CommonParser.read_file(args.users)
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
