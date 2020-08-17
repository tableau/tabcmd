
import sys
from .parent_parser import ParentParser


class LogoutParser:
    """ Parses logout arguments passed by the user"""

    @staticmethod
    def logout_parser():
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        logout_parser = subparsers.add_parser('logout', parents=[parser])
        args = logout_parser.parse_args(sys.argv[2:])
        return args
