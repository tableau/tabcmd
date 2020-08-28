import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser


class DecryptExtractsParser:
    @staticmethod
    def decrypt_extracts_parser():
        """Method to parse decrypt extracts arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        decrypt_extract_parser = subparsers.add_parser('decryptextracts',
                                                       parents=[parser])
        site_name = sys.argv[2]
        args = decrypt_extract_parser.parse_args(sys.argv[2:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args, site_name
