from .global_options import *


class RefreshExtractsParser:
    """
    Parser to refreshextracts command
    """

    @staticmethod
    def refresh_extracts_parser(manager, command):
        """Method to parse refresh extracts arguments passed by the user"""
        refresh_extract_parser = manager.include(command)
        target_group = refresh_extract_parser.add_mutually_exclusive_group(required=True)
        target_group.add_argument('--datasource')
        target_group.add_argument('--workbook')

        set_incremental_options(refresh_extract_parser)
        set_calculations_options(refresh_extract_parser)
        set_project_arg(refresh_extract_parser)
        set_parent_project_arg(refresh_extract_parser)
        refresh_extract_parser.add_argument(
            '--url',
            help='The name of the workbook as it appears in the URL. A workbook published as “Sales Analysis” \
            has a URL name of “SalesAnalysis”.')
