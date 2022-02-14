import sys
from tabcmd.execution.parent_parser import ParentParser


class EncryptExtractsParser:
    """
    Parser for the command encryptextracts
    """
    USER_ARG_IDX = 2

    @staticmethod
    def encrypt_extracts_parser():
        """Method to parse encrypt extracts arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        encrypt_extract_parser = subparsers.add_parser('encryptextracts', parents=[parser])
        args = encrypt_extract_parser.parse_args(sys.argv[ EncryptExtractsParser.USER_ARG_IDX:])
        args.site_name = sys.argv[2]
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
