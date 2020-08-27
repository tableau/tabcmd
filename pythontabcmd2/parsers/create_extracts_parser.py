import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser


class CreateExtractsParser:
    @staticmethod
    def create_extracts_parser():
        """Method to parse create extracts arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        create_group_parser = subparsers.add_parser('createextracts',
                                                    parents=[parser])
        create_group_parser.add_argument('--datasource', '-d',
                                         help='name of datasource')
        args = create_group_parser.parse_args(sys.argv[2:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
