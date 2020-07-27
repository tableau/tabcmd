import argparse
import sys
from .global_options import *


class AddUserParser:
    @staticmethod
    def add_user_parser():
        """Method to parse create user arguments passed """
        parser = argparse.ArgumentParser(description='add user to group command')
        parser.add_argument('--group', '-g', required=True, help='name of group')
        parser.add_argument('--file', '-f', required=True, help='csv containing user details', type=argparse.FileType('r'))
        args = parser.parse_args(sys.argv[2:])
        csv_lines = [line.strip() for line in args.file.readlines()]
        args.file.close()
        return csv_lines, args
