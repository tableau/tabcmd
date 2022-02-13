import sys
from .parent_parser import ParentParser
from .common_parser import CommonParser


class CreateSiteUsersParser:
    """
    Parser for createsiteusers command
    """
    USER_ARG_IDX = 3
    USER_ARG_FILE_NAME_IDX = 2

    @staticmethod
    def create_site_user_parser():
        """Method to parse create site users arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        create_site_users_parser = subparsers.add_parser('createsiteusers', parents=[parser])
        create_site_users_parser.add_argument('--role', '-r', default="Unlicensed", help='name of site')
        args = create_site_users_parser.parse_args(sys.argv[CreateSiteUsersParser.USER_ARG_IDX:])
        args.csv_lines = CommonParser.read_file(sys.argv[CreateSiteUsersParser.USER_ARG_FILE_NAME_IDX])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
