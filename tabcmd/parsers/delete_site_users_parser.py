import sys
from .parent_parser import ParentParser
from .common_parser import CommonParser


class DeleteSiteUsersParser:
    """
    Parser for the command deletesiteusers
    """
    USER_ARG_FILE_NAME_IDX = 2
    USER_ARG_IDX = 3

    @staticmethod
    def delete_site_users_parser():
        """Method to parse delete site arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        delete_site_users_parser = subparsers.add_parser('deletesiteusers', parents=[parser])
        args = delete_site_users_parser.parse_args(sys.argv[DeleteSiteUsersParser.USER_ARG_IDX:])
        args.csv_lines = CommonParser.read_file(sys.argv[DeleteSiteUsersParser.USER_ARG_FILE_NAME_IDX])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
