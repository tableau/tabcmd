import argparse
import sys
import shlex
import getpass

from .global_options import *
    
class CreateGroupParser:
    def create_group_parser(self):
        parser = argparse.ArgumentParser(description='create group command')
        parser.add_argument('--name','-n', required=True, help='name of group')
        args = parser.parse_args(sys.argv[2:])
        return args.name


