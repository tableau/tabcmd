import sys
from .parent_parser import ParentParser
from .common_parser import CommonParser


class DeleteUserParser:
    @staticmethod
    def delete_user_parser():
        """Method to parse delete user arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        delete_users_parser = subparsers.add_parser('deleteusers',
                                                    parents=[parser])
        args = delete_users_parser.parse_args(sys.argv[3:])
        csv_lines = CommonParser.read_file(sys.argv[2])
        return csv_lines, args
# TODO: ARGUMENT --COMPLETE
