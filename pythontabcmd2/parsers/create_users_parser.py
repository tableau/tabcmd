import argparse
import sys
from .global_options import *


class CreateUserParser:
    @staticmethod
    def create_user_parser():
        """Method to parse create user arguments passed """
        parser = argparse.ArgumentParser(description='create group command')
        parser.add_argument('--file', '-f', required=True, help='csv containing user details', type=argparse.FileType('r'))
        args = parser.parse_args(sys.argv[2:])
        csv_lines = [line.strip() for line in args.file.readlines()]
        args.file.close()
        return csv_lines
