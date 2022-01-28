import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser


class ReencryptExtractsParser:
    """
    Parser to reencrypt command
    """
    @staticmethod
    def reencrypt_extracts_parser():
        """Method to parse reencrypt extracts arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        reencrypt_extract_parser = subparsers.add_parser('reencryptextracys',
                                                         parents=[parser])
        site_name = sys.argv[2]
        args = reencrypt_extract_parser.parse_args(sys.argv[3:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args, site_name
