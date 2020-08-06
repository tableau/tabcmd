import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser


class CreateGroupParser:
    @staticmethod
    def create_group_parser():
        """Method to parse create group arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        create_group_parser = subparsers.add_parser('creategroup',
                                                    parents=[parser])
        create_group_parser.add_argument('--name', '-n',
                                         required=True, help='name of group')
        args = create_group_parser.parse_args(sys.argv[2:])
        return args
