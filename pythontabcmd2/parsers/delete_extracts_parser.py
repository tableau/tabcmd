import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser


class DeleteExtractsParser:
    @staticmethod
    def delete_extracts_parser():
        """Method to parse delete extracts arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        delete_extract_parser = subparsers.add_parser('deleteextracts',
                                                      parents=[parser])
        delete_extract_parser.add_argument('--datasource', '-d',
                                           help='name of datasource')
        delete_extract_parser.add_argument('--embedded-datasources',
                                           help='A space-separated list'
                                                'of embedded data source '
                                                'names within the target'
                                                ' workbook. ')
        delete_extract_parser.add_argument('--encrypt',
                                           help='Create encrypted extract')
        delete_extract_parser.add_argument('--include-all',
                                           help='Include all embedded data '
                                                'sources within target'
                                                ' workbook. Only available '
                                                'when creating extracts '
                                                'for workbook.')
        delete_extract_parser.add_argument('--project',
                                           help='The name of the project'
                                                ' that contains the target '
                                                'resource')
        delete_extract_parser.add_argument('--url', '-u',
                                           help='The canonical name for the '
                                                'resource as it appears'
                                                ' in the URL')
        delete_extract_parser.add_argument('--workbook', '-w',
                                           help='The name of the target '
                                                'workbook for extract '
                                                'creation.')
        args = delete_extract_parser.parse_args(sys.argv[2:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
