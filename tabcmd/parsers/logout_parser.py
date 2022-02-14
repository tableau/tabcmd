
import sys
from tabcmd.execution.parent_parser import ParentParser


class LogoutParser:
    """ Parses logout arguments passed by the user"""
    USER_ARG_IDX = 2

    @staticmethod
    def logout_parser():
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        logout_parser = subparsers.add_parser('logout', parents=[parser])
        args = logout_parser.parse_args(sys.argv[LogoutParser.USER_ARG_IDX:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
