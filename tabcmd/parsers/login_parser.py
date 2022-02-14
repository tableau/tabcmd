import sys
import getpass
from ..execution.logger_config import get_logger
from tabcmd.execution.parent_parser import ParentParser

logger = get_logger('tabcmd.login_parser', 'info')


class LoginParser:
    """ Parses login arguments passed by the user"""
    USER_ARG_IDX = 2

    @staticmethod
    def login_parser():

        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()

        subparsers = parser.add_subparsers()
        login_parser = subparsers.add_parser('login', parents=[parser])
        args = login_parser.parse_args(sys.argv[LoginParser.USER_ARG_IDX:])

        if args.username and not args.password:
            if args.prompt:
                args.password = getpass.getpass("Password:")
            else:
                logger.error("Please provide password")
                sys.exit()
        if args.token_name and not args.token:
            if args.prompt:
                args.token = getpass.getpass("Token:")
            else:
                logger.error("Please provide password")
                sys.exit()

        if args.site is None or args.site == "Default":
            args.site = ''
        return args
