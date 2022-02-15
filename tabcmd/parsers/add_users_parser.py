import sys
from tabcmd.execution.parent_parser import ParentParser
from tabcmd.execution.common_parser import CommonParser


class AddUserParser:
    """
    Parser for AddUser command
    """

    @staticmethod
    def add_user_parser(manager, command):
        """Method to parse add user arguments passed """

        add_user_parser = manager.include(command)
        add_user_parser.add_argument('groupname', help='name of group to add users to')

        add_user_parser.add_argument('--users', required=True, help='csv containing user details')
        args = add_user_parser.parse_args(sys.argv[AddUserParser.USER_ARG_IDX:])
        args.group_name = sys.argv[AddUserParser.USER_GROUP_ARG_IDX]
        args.csv_lines = CommonParser.read_file(args.users)
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
    