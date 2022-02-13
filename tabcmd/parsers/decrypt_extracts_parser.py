import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser


class DecryptExtractsParser:
    """
    Parser for the command decryptextracts
    """
    USER_ARG_IDX = 2
    USER_ARG_SITE_NAME_IDX = 2

    @staticmethod
    def decrypt_extracts_parser():
        """Method to parse decrypt extracts arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        decrypt_extract_parser = subparsers.add_parser('decryptextracts', parents=[parser])
        args = decrypt_extract_parser.parse_args(sys.argv[DecryptExtractsParser.USER_ARG_IDX:])

        args.site_name = sys.argv[DecryptExtractsParser.USER_ARG_SITE_NAME_IDX]
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
