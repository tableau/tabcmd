import argparse
import sys
import shlex
import getpass
try:
    from .global_options import *
except ModuleNotFoundError:
    from parsers.global_options import *


class DeleteGroupParser:
    def delete_group_parser(self):
        """Method to parse delete group arguments passed by the user"""
        parser = argparse.ArgumentParser(description='delete group command')
        parser.add_argument('--name','-n', required=True, help='name of group to delete')
        args = parser.parse_args(sys.argv[2:])
        return args.name