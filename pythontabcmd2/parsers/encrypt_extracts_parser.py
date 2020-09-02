import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser
from .common_parser import CommonParser


class EncryptExtractsParser:
    @staticmethod
    def encrypt_extracts_parser():
        """Method to parse encrypt extracts arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        encrypt_extract_parser = subparsers.add_parser('encryptextracts',
                                                       parents=[parser])
        site_name = sys.argv[2]
        args = encrypt_extract_parser.parse_args(sys.argv[3:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args, site_name
