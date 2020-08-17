import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser
from .common_parser import CommonParser


class PublishSamplesParser(ParentParser):

    @staticmethod
    def publish_samples_parser():
        """Method to parse publish samples arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        common_parser_obj = CommonParser()

        common_parser = common_parser_obj.common_parser_arguments()
        subparsers = parser.add_subparsers()
        publish_samples_parser = subparsers.add_parser('publishsamples',
                                                       parents=[parser,
                                                                common_parser])
        publish_samples_parser.add_argument('--name', '-n', required=True,
                                            help='name of project')

        args = publish_samples_parser.parse_args(sys.argv[2:])
        if args.parent_project_path is not None:
            evaluated_project_path = GlobalOptions. \
                evaluate_project_path(args.parent_project_path)
        else:
            evaluated_project_path = args.parent_project_path
        if args.site is None or args.site == "Default":
            args.site = ''
        return args, evaluated_project_path
