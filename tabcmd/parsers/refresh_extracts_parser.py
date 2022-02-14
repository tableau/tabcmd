import sys
from tabcmd.execution.parent_parser import ParentParser
from tabcmd.execution.common_parser import CommonParser


class RefreshExtractsParser:
    """
    Parser to refreshextracts command
    """
    USER_ARG_IDX = 2

    @staticmethod
    def refresh_extracts_parser():
        """Method to parse refresh extracts arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        common_parser_obj = CommonParser()
        common_parser = common_parser_obj.common_parser_arguments()
        subparsers = parser.add_subparsers()
        refresh_extract_parser = subparsers.add_parser('refreshextracts',
                                                       parents=[parser,
                                                                common_parser])
        refresh_extract_parser.add_argument('--datasource',
                                            help='The name of the data source'
                                                 ' containing extracts'
                                                 ' to refresh')
        refresh_extract_parser.add_argument('--incremental',
                                            help='Runs the incremental '
                                                 'refresh operation')
        refresh_extract_parser.add_argument('--synchronous',
                                            help='Adds the full refresh'
                                                 ' operation to the queue used'
                                                 ' by the Backgrounder '
                                                 'process,'
                                                 ' to be run as soon as a'
                                                 ' Backgrounder process'
                                                 ' is available.')
        refresh_extract_parser.add_argument('--addcalculations',
                                            help='Use with --workbook to '
                                                 'materialize calculations in '
                                                 'the embedded extract of the '
                                                 'workbook or --datasource to '
                                                 'materialize calculations in '
                                                 'the extract data source')
        refresh_extract_parser.add_argument('--removecalculations',
                                            help='Use with --workbook or '
                                                 '--datasource to remove '
                                                 'calculations that were'
                                                 ' previously materialized')
        refresh_extract_parser.add_argument('--project',
                                            help='The name of the project'
                                                 ' that contains the target '
                                                 'resource')
        refresh_extract_parser.add_argument('--url',
                                            help='The name of the workbook '
                                                 'as it appears in the URL.'
                                                 ' A workbook published as '
                                                 '“Sales Analysis” has a URL '
                                                 'name of “SalesAnalysis”.')
        refresh_extract_parser.add_argument('--workbook',
                                            help='The name of the workbook'
                                                 ' containing extracts to '
                                                 'refresh. If the '
                                                 'workbook has '
                                                 'spaces in its name, enclose '
                                                 'it in quotes')
        args = refresh_extract_parser.parse_args(sys.argv[
                                                 RefreshExtractsParser.
                                                 USER_ARG_IDX:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
