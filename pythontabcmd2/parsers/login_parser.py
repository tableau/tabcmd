import argparse
import sys
import getpass
from .global_options import *
from ..logger_config import get_logger
from .parent_parser import ParentParser

logger = get_logger('pythontabcmd2.login_parser', 'info')


class LoginParser:
    """ Parses login arguments passed by the user"""

    @staticmethod
    def login_parser():

        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()

        subparsers = parser.add_subparsers()
        login_parser = subparsers.add_parser('login', parents=[parser])
        args = login_parser.parse_args(sys.argv[2:])

        if args.prompt and args.username:
            args.password = getpass.getpass("Password:")
        if args.prompt and args.token_name:
            args.token = getpass.getpass("Token:")
        if args.no_prompt and args.username and args.password is None:
            logger.error("Please provide password")
            sys.exit()
        if args.no_prompt and args.token_name and args.token is None:
            logger.error("Please provide token")
            sys.exit()
        if args.username and args.password is None:
            args.password = getpass.getpass("Password:")
        if args.token_name and args.token is None:
            args.token = getpass.getpass("Token:")
        if args.site is None:
            args.site = ''
        return args
