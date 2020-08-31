import argparse
import sys
from .parent_parser import ParentParser
from .common_parser import CommonParser


class GetUrlParser:

    @staticmethod
    def get_url_parser():
        """Method to parse get url arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        common_parser_obj = CommonParser()

        common_parser = common_parser_obj.common_parser_arguments()
        subparsers = parser.add_subparsers()
        delete_parser = subparsers.add_parser(
            'get',
            parents=[parser])
        delete_parser.add_argument('--filename', '-f',
                                   help='name of the file')
        args = delete_parser.parse_args(sys.argv[2:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
