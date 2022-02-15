import sys
from tabcmd.execution.parent_parser import ParentParser


class ExportParser:
    """
    Parser for the command export
    """

    @staticmethod
    def export_parser(manager, command):
        """Method to parse export arguments passed by the user"""
        export_parser = manager.include(command)
        export_parser.add_argument('url', help='url of the workbook or view to export')

        export_parser_group = export_parser.add_mutually_exclusive_group(required=True)
        export_parser_group.add_argument('--pdf', action='store_true', help="pdf of a view")
        export_parser_group.add_argument('--fullpdf', action='store_true', help="fullpdf of workbook")
        export_parser_group.add_argument('--png', action='store_true', help="png of a view")
        export_parser_group.add_argument('--csv', action='store_true', help="csv of a view")

        export_parser.add_argument(
            '--pagelayout', choices=['landscape', 'portrait'], default="landscape",
            help='page orientation (landscape or portrait) of the exported PDF')
        export_parser.add_argument('--pagesize', default="letter", help='Set the page size of the exported PDF')
        export_parser.add_argument('--width', default=800, help='Set the width in pixels. Default is 800 px')
        export_parser.add_argument('--filename', '-f', help='filename to store the exported data')
        export_parser.add_argument('--height', default=600, help='Sets the height in pixels. Default is 600 px')
        export_parser.add_argument('--filter', '-vf', metavar='COLUMN:VALUE', help='View filter to apply to the view')


# TODO: ARGUMENT --COMPLETE
