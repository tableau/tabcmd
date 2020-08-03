import argparse
import sys
from .global_options import *


class DeleteSiteParser:

    @staticmethod
    def delete_site_parser():
        """Method to parse delete site arguments passed by the user"""
        parser = argparse.ArgumentParser(description='delete site command')
        parser.add_argument('--site-name', '-s', required=True,
                            help='name of site to delete')
        parser.add_argument('--logging-level', '-l',
                            choices=['debug', 'info', 'error'], default='error',
                            help='desired logging level (set to error by default)')
        args = parser.parse_args(sys.argv[2:])
        return args

# TODO: COMPLETE, NO COMPLETE OPTION, GLOBAL SITE OPTION
