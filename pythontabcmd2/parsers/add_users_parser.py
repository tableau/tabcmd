import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser


class AddUserParser:
    @staticmethod
    def add_user_parser():
        """Method to parse create user arguments passed """
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        add_user_parser = subparsers.add_parser('adduser',
                                                parents=[parser])
        add_user_parser.add_argument('--group', '-g',
                                     required=True, help='name of group')
        add_user_parser.add_argument('--users',
                                     required=True,
                                     help='csv containing user details',
                                     type=argparse.FileType('r'))
        args = add_user_parser.parse_args(sys.argv[2:])
        csv_lines = [line.strip() for line in args.file.readlines()]
        args.file.close()
        return csv_lines, args
