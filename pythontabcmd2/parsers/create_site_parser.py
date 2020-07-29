import argparse
import sys
from .global_options import *


class CreateSiteParser:

    @staticmethod
    def create_site_parser():
        """Method to parse create site arguments passed by the user"""
        parser = argparse.ArgumentParser(description='create site command')
        parser.add_argument('--site-name', '-s', required=True,
                            help='name of site')
        parser.add_argument('--url', '-r', default=None,
                            help='used in URLs to specify site')
        parser.add_argument('--user-quota', '-u', type=int, default=None,
                            help='Max number of user that '
                                 'can be added to site')
        parser.add_argument('--storage-quota', '-q', type=int, default=None,
                            help='in MB amount of workbooks, extracts data '
                                 'sources stored on site')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--site-mode', '-m',
                           default=None,
                           help='Does not allow site admins '
                                'to add or remove users')
        group.add_argument('--no-site-mode', '-n', default=None,
                           help='Allows site admins to add or remove users')
        args = parser.parse_args(sys.argv[2:])

        admin_mode = None
        if args.no_site_mode:
            admin_mode = "ContentOnly"
        if args.site_mode:
            admin_mode = "ContentAndUsers"
        return args, admin_mode

# TODO: EXTRACT ENCRYPTIONN MODE, RUN NOW ENABLED,
