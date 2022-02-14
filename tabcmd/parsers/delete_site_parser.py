import sys
from tabcmd.execution.parent_parser import ParentParser


class DeleteSiteParser:
    """
    Parser for the command deletesite
    """
    USER_ARG_IDX = 2

    @staticmethod
    def delete_site_parser():
        """Method to parse delete site arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        delete_site_parser = subparsers.add_parser('deletesite',
                                                   parents=[parser])
        delete_site_parser.add_argument('--site-name', default=None,
                                        help='name of site to delete')
        args = delete_site_parser.parse_args(sys.argv[3:])
        if args.site_name is None:
            args.site_name = sys.argv[2]
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
