import sys
from tabcmd.execution.parent_parser import ParentParser


class ListSitesParser:
    """
    Parser to list sites
    """
    USER_ARG_IDX = 2

    @staticmethod
    def list_site_parser():
        """Method to parse list sites arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        edit_site_parser = subparsers.add_parser('listsites',
                                                 parents=[parser])
        edit_site_parser.add_argument('--extract-encryption-mode',
                                      default=None,
                                      help='The extract encryption mode for '
                                           'the site can be enforced, '
                                           'enabled or disabled')
        args = edit_site_parser.parse_args(sys.argv[ListSitesParser.
                                                    USER_ARG_IDX:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
