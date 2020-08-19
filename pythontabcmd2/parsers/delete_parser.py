import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser
from .common_parser import CommonParser

class DeleteDataSourceParser:

    @staticmethod
    def delete_data_source_parser():
        """Method to parse delete data source arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        common_parser_obj = CommonParser()

        common_parser = common_parser_obj.common_parser_arguments()
        subparsers = parser.add_subparsers()
        delete_data_source_parser = subparsers.add_parser(
                                        'deletedatasource_or_deleteworkbook',
                                                    parents=[parser, common_parser])
        delete_group = delete_data_source_parser.add_mutually_exclusive_group()
        delete_group.add_argument('--datasource',
                                         help='name of group to delete')
        delete_group.add_argument('--workbook',
                                         help='name of group to delete')
        delete_data_source_parser.add_argument('--project', '-r',
                                         help='name of group to delete')

        args = delete_data_source_parser.parse_args(sys.argv[2:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
