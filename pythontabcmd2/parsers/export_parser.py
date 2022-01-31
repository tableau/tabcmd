import argparse
import sys
from .parent_parser import ParentParser
from .common_parser import CommonParser


class ExportParser:
    """
    Parser for the command export
    """
    USER_ARG_IDX = 3
    USER_ARG_URL_IDX = 2

    @staticmethod
    def export_parser():
        """Method to parse export arguments passed by the user"""
        url = ""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        export_parser = subparsers.add_parser('export',
                                              parents=[parser])
        export_parser_group = export_parser.add_mutually_exclusive_group(
            required=True)
        export_parser_group.add_argument('--pdf', action='store_true',
                                         help="pdf of a view")
        export_parser_group.add_argument('--fullpdf', action='store_true',
                                         help="fullpdf of workbook")
        export_parser_group.add_argument('--png', action='store_true',
                                         help="png of a view")
        export_parser_group.add_argument('--csv', action='store_true',
                                         help="csv of a view")
        export_parser.add_argument('--pagelayout', default="landscape",
                                   help='page orientation (landscape or '
                                        'portrait) of '
                                        'the exported PDF')
        export_parser.add_argument('--pagesize', default="letter",
                                   help='Set the page size of the '
                                        'exported PDF')
        export_parser.add_argument('--width', default=800,
                                   help='Set the width in pixels. Default is '
                                        '800 px')
        export_parser.add_argument('--filename', '-f',
                                   help='filename to store the exported data')
        export_parser.add_argument('--height', default=600,
                                   help='Sets the height in pixels. Default '
                                        'is 600 px')
        export_parser.add_argument('--filter', '-vf', metavar='COLUMN:VALUE',
                                   help='View filter to apply to the view')
        args = export_parser.parse_args(sys.argv[ExportParser.USER_ARG_IDX:])
        try:
            url = sys.argv[ExportParser.USER_ARG_URL_IDX]
        except Exception as ex:
            print(ex)
            print("Please enter a valid URL")
            sys.exit()
        if args.site is None or args.site == "Default":
            args.site = ''
        return args, url

# TODO: ARGUMENT --COMPLETE
