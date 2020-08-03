import argparse
import sys
from .global_options import *


class RemoveUserParser:

    @staticmethod
    def remove_user_parser():
        """Method to parse remove user arguments passed by the user"""
        parser = argparse.ArgumentParser(description='remove user command')
        parser.add_argument('--group', '-g', required=True,
                            help='name of group')
        parser.add_argument('--file', '-f', required=True,
                            help='csv containing user details',
                            type=argparse.FileType('r'))
        parser.add_argument('--logging-level', '-l',
                            choices=['debug', 'info', 'error'], default='error',
                            help='desired logging level'
                                 ' (set to error by default)')
        args = parser.parse_args(sys.argv[2:])
        csv_lines = [line.strip() for line in args.file.readlines()]
        args.file.close()
        return csv_lines, args


# TODO: ARGUMENT --COMPLETE
