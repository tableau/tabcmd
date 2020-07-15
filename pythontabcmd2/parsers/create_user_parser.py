import argparse
import sys
import csv
import getpass
try:
    from .global_options import *
except:
    from parsers.global_options import *


class CreateUserParser:
    def create_user_parser(self):
        """Method to parse create user arguments passed """
        parser = argparse.ArgumentParser(description='create group command')
        parser.add_argument('--file', '-f', required=True, help='csv containing user details', type=argparse.FileType('r'))
        args = parser.parse_args(sys.argv[2:])
        csv_lines = [line.strip() for line in args.file.readlines()]
        return csv_lines


    def parse_lines(self, csv_lines):
        pass