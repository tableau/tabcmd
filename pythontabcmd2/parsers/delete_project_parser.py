import argparse
import sys
from .global_options import *


class DeleteProjectParser:
    @staticmethod
    def delete_project_parser():
        """Method to parse delete project arguments passed by the user"""
        parser = argparse.ArgumentParser(description='delete project command')
        parser.add_argument('--name', '-n', required=True,
                            help='name of project to delete')
        parser.add_argument('--parent-project-path', '-p', default=None,
                            help='path of parent project')
        parser.add_argument('--logging-level', '-l',
                            choices=['debug', 'info', 'error'], default='error',
                            help='desired logging level (set to error by default)')
        args = parser.parse_args(sys.argv[2:])
        if args.parent_project_path is not None:
            evaluated_project_path = \
                GlobalOptions.evaluate_project_path(args.parent_project_path)
        else:
            evaluated_project_path = args.parent_project_path
        return args, evaluated_project_path
