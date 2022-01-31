import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser
from .common_parser import CommonParser


class CreateExtractsParser:
    """
    Parser for createextracts command
    """
    USER_ARG_IDX = 2

    @staticmethod
    def create_extracts_parser():
        """Method to parse create extracts arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        common_parser_obj = CommonParser()
        common_parser = common_parser_obj.common_parser_arguments()
        subparsers = parser.add_subparsers()
        create_extract_parser = subparsers.add_parser('createextracts',
                                                      parents=[parser,
                                                               common_parser])
        create_extract_parser.add_argument('--datasource', '-d',
                                           help='name of datasource')
        create_extract_parser.add_argument('--embedded-datasources',
                                           help='A space-separated list'
                                                'of embedded data source '
                                                'names within the target'
                                                ' workbook. ')
        create_extract_parser.add_argument('--encrypt',
                                           help='Create encrypted extract')
        create_extract_parser.add_argument('--include-all',
                                           help='Include all embedded data '
                                                'sources within target'
                                                ' workbook. Only available '
                                                'when creating extracts '
                                                'for workbook.')
        create_extract_parser.add_argument('--project',
                                           help='The name of the project'
                                                ' that contains the target '
                                                'resource')
        create_extract_parser.add_argument('--url',
                                           help='The canonical name for the '
                                                'resource as it appears'
                                                ' in the URL')
        create_extract_parser.add_argument('--workbook', '-w',
                                           help='The name of the target '
                                                'workbook for extract '
                                                'creation.')
        args = create_extract_parser.parse_args(sys.argv[
                                                CreateExtractsParser.
                                                USER_ARG_IDX:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
