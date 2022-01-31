import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser
from .common_parser import CommonParser


class DeleteProjectParser:
    """
    Parser for the command deleteproject
    """
    USER_ARG_IDX = 2

    @staticmethod
    def delete_project_parser():
        """Method to parse delete project arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        common_parser_obj = CommonParser()

        common_parser = common_parser_obj.common_parser_arguments()
        subparsers = parser.add_subparsers()
        delete_project_parser = subparsers.add_parser('deleteproject',
                                                      parents=[parser,
                                                               common_parser])
        delete_project_parser.add_argument('--name', '-n', required=True,
                                           help='name of project to delete')
        args = delete_project_parser.parse_args(sys.argv[
                                                DeleteProjectParser.
                                                USER_ARG_IDX:])
        if args.parent_project_path is not None:
            evaluated_project_path = \
                GlobalOptions.evaluate_project_path(args.parent_project_path)
        else:
            evaluated_project_path = args.parent_project_path
        if args.site is None or args.site == "Default":
            args.site = ''
        return args, evaluated_project_path
