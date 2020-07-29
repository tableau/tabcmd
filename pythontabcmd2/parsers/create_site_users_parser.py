import argparse
import sys
from .global_options import *


class CreateSiteUsersParser:

    @staticmethod
    def create_site_user_parser():
        """Method to parse create site users arguments passed by the user"""
        parser = argparse.ArgumentParser(
            description='create site users command')
        parser.add_argument('--role', '-r',
                            default="Unlicensed", help='name of site')
        parser.add_argument('--file', '-f', required=True,
                            help='csv containing user details',
                            type=argparse.FileType('r'))
        args = parser.parse_args(sys.argv[2:])
        csv_lines = [line.strip() for line in args.file.readlines()]
        args.file.close()
        return csv_lines, args.role

# TODO: COMPLETE, NOCOMPLETE OPTION, GLOBAL SITE OPTION
