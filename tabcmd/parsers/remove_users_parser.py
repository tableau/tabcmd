import sys
from tabcmd.execution.parent_parser import ParentParser
from tabcmd.execution.common_parser import CommonParser


class RemoveUserParser:
    """
    Parser to removeusers command
    """
    USER_ARG_IDX = 3
    USER_ARG_GROUP_NAME_IDX = 2

    @staticmethod
    def remove_user_parser():
        """Method to parse remove user arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        remove_users_parser = subparsers.add_parser('removeusers', parents=[parser])

        remove_users_parser.add_argument('--users', required=True, help='csv containing user details')
        args = remove_users_parser.parse_args(sys.argv[RemoveUserParser.USER_ARG_IDX:])
        args.group_name = sys.argv[RemoveUserParser.USER_ARG_GROUP_NAME_IDX]
        args.csv_lines = CommonParser.read_file(args.users)
        if args.site is None or args.site == "Default":
            args.site = ''
        return args

# TODO: ARGUMENT --COMPLETE
