from .global_options import *


class GetUrlParser:
    """Parser for the command geturl"""

    @staticmethod
    def get_url_parser(manager, command):
        """Method to parse get url arguments passed by the user"""
        get_url_parser = manager.include(command)
        get_url_parser.add_argument('url', help='url that identifies the view or workbook to export')
        set_filename_arg(get_url_parser)
        # png size in pixels, refresh are both just set on the url
