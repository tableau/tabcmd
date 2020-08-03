import argparse
import sys
from .global_options import *


class DeleteGroupParser:

    @staticmethod
    def delete_group_parser():
        """Method to parse delete group arguments passed by the user"""
        parser = argparse.ArgumentParser(description='delete group command')
        parser.add_argument('--name', '-n', required=True,
                            help='name of group to delete')
        parser.add_argument('--logging-level', '-l',
                            choices=['debug', 'info', 'error'], default='error',
                            help='desired logging level (set to error by default)')
        args = parser.parse_args(sys.argv[2:])
        return args
