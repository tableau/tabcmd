import argparse
import sys
from .global_options import *


class CreateGroupParser:
    @staticmethod
    def create_group_parser():
        """Method to parse create group arguments passed by the user"""
        parser = argparse.ArgumentParser(description='create group command')
        parser.add_argument('--name', '-n',
                            required=True, help='name of group')
        parser.add_argument('--logging-level', '-l',
                            choices=['debug', 'info', 'error'], default='error',
                            help='desired logging '
                                 'level (set to error by default)')
        args = parser.parse_args(sys.argv[2:])
        return args
