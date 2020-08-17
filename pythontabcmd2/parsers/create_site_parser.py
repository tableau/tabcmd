import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser


class CreateSiteParser:
    @staticmethod
    def create_site_parser():
        """Method to parse create site arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        create_site_parser = subparsers.add_parser('createsite',
                                                   parents=[parser])
        create_site_parser.add_argument('--site-name', default=None,
                                        help='name of site')
        create_site_parser.add_argument('--url', '-r', default=None,
                                        help='used in URLs to specify site')
        create_site_parser.add_argument('--user-quota', type=int, default=None,
                                        help='Max number of user that '
                                             'can be added to site')
        create_site_parser.add_argument('--storage-quota', type=int,
                                        default=None,
                                        help='in MB amount of workbooks, '
                                             'extracts data '
                                             'sources stored on site')
        group = create_site_parser.add_mutually_exclusive_group()
        group.add_argument('--site-mode',
                           default=None,
                           help='Does not allow site admins '
                                'to add or remove users')
        group.add_argument('--no-site-mode', default=None,
                           help='Allows site admins to add or remove users')
        args = create_site_parser.parse_args(sys.argv[3:])
        if args.site_name is None:
            args.site_name = sys.argv[2]
        admin_mode = None
        if args.no_site_mode:
            admin_mode = "ContentOnly"
        if args.site_mode:
            admin_mode = "ContentAndUsers"
        if args.site is None or args.site == "Default":
            args.site = ''
        return args, admin_mode

# TODO: EXTRACT ENCRYPTIONN MODE, RUN NOW ENABLED,
