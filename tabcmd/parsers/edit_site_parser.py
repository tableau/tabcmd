import sys
from .parent_parser import ParentParser


class EditSiteParser:
    """
    Parser for the command editsite
    """
    USER_ARG_SITE_ID_START_IDX = 2
    USER_ARG_SITE_ID_END_IDX = 3
    USER_ARG_IDX = 3

    @staticmethod
    def edit_site_parser():
        """Method to parse edit site arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        edit_site_parser = subparsers.add_parser('editsite', parents=[parser])
        edit_site_parser.add_argument('--site-name', default=None, help='name of site')
        edit_site_parser.add_argument('--site-id', default=None, help='id of site')
        edit_site_parser.add_argument('--url', default=None, help='url of site')
        edit_site_parser.add_argument(
            '--user-quota', type=int, default=None, help='Max number of user that can be added to site')
        edit_site_parser.add_argument(
            '--status', default=None, help='Set to ACTIVE to activate a site, or to SUSPENDED to suspend a site.')
        edit_site_parser.add_argument(
            '--extract-encryption-mode', default=None,
            help='The extract encryption mode for the site can be enforced, enabled or disabled')
        edit_site_parser.add_argument(
            '--run-now-enabled', default=None,
            help='Allow or deny users from running extract refreshes, flows, or schedules manually.')
        edit_site_parser.add_argument(
            '--storage-quota', type=int, default=None,
            help='in MB amount of workbooks, extracts data sources stored on site')
        group = edit_site_parser.add_mutually_exclusive_group()
        group.add_argument('--site-mode', default=None, help='Does not allow site admins to add or remove users')
        group.add_argument('--no-site-mode', default=None, help='Allows site admins to add or remove users')
        args = edit_site_parser.parse_args(sys.argv[EditSiteParser.USER_ARG_IDX:])
        current_site_id_as_list = sys.argv[EditSiteParser.USER_ARG_SITE_ID_START_IDX:EditSiteParser.USER_ARG_SITE_ID_END_IDX]
        args.current_site_id = ''.join(current_site_id_as_list)
        args.admin_mode = None
        if args.no_site_mode:
            args.admin_mode = "ContentOnly"
        if args.site_mode:
            args.admin_mode = "ContentAndUsers"
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
