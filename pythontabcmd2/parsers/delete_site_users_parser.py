import sys
from .parent_parser import ParentParser
from .common_parser import CommonParser


class DeleteSiteUsersParser:
    """
    Parser for the command deletesiteusers
    """
    @staticmethod
    def delete_site_users_parser():
        """Method to parse delete site arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        delete_site_users_parser = subparsers.add_parser('deletesiteusers',
                                                         parents=[parser])
        args = delete_site_users_parser.parse_args(sys.argv[3:])
        csv_lines = CommonParser.read_file(sys.argv[2])
        if args.site is None or args.site == "Default":
            args.site = ''
        return csv_lines, args
