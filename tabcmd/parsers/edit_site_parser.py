from .global_options import *


class EditSiteParser:
    """
    Parser for the command editsite
    """

    @staticmethod
    def edit_site_parser(manager, command):
        """Method to parse edit site arguments passed by the user"""
        edit_site_parser = manager.include(command)
        edit_site_parser.add_argument("site_name", metavar="site-name", help="name of site to update")
        edit_site_parser.add_argument(
            "--site-name", default=None, dest="new_site_name", help="The name of the site that's displayed."
        )

        set_common_site_args(edit_site_parser)
        set_site_status_arg(edit_site_parser)
