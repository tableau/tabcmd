import argparse
import sys
import shlex
import getpass
try:
    from .global_options import *
except:
    from parsers.global_options import *

class CreateGroupParser:
    def create_group_parser(self):
        """Method to parse create group arguments passed by the user"""
        parser = argparse.ArgumentParser(description='create group command')
        parser.add_argument('--name','-n', required=True, help='name of group')
        args = parser.parse_args(sys.argv[2:])
        return args.name


