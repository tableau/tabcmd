import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser


class ReencryptExtractsParser:
    """
    Parser to reencrypt command
    """
    USER_ARG_IDX = 2
    USER_ARG_SITE_NAME_IDX = 2

    @staticmethod
    def reencrypt_extracts_parser():
        """Method to parse reencrypt extracts arguments passed by the user"""
        site_name = ""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        reencrypt_extract_parser = subparsers.add_parser('reencryptextracys', parents=[parser])
        args = reencrypt_extract_parser.parse_args(sys.argv[ReencryptExtractsParser.USER_ARG_IDX:])
        try:
            site_name = sys.argv[ReencryptExtractsParser.USER_ARG_SITE_NAME_IDX]
        except Exception as ex:
            print(ex)

        if args.site is None or args.site == "Default":
            args.site = ''
        return args, site_name
