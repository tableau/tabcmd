import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser


class DeleteGroupParser:
    """
    Parser for the command deletegroup
    """
    USER_ARG_IDX = 2

    @staticmethod
    def delete_group_parser():
        """Method to parse delete group arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        delete_group_parser = subparsers.add_parser('deletegroup',
                                                    parents=[parser])
        delete_group_parser.add_argument('--name', '-n', required=True,
                                         help='name of group to delete')

        args = delete_group_parser.parse_args(sys.argv[DeleteGroupParser.
                                              USER_ARG_IDX:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
