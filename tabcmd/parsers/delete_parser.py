import sys
from tabcmd.execution.parent_parser import ParentParser
from tabcmd.execution.common_parser import CommonParser


class DeleteParser:
    """Parser for the command delete"""
    USER_ARG_IDX = 2

    @staticmethod
    def delete_parser():
        """Method to parse delete data source arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        common_parser_obj = CommonParser()

        common_parser = common_parser_obj.common_parser_arguments()
        subparsers = parser.add_subparsers()
        delete_parser = subparsers.add_parser(
            'deletedatasource_or_deleteworkbook',
            parents=[parser, common_parser])
        delete_parser.add_argument('--project', '-r', default=None,
                                   help='name of project to delete')
        delete_parser.add_argument('--datasource', default=None,
                                   help='name of datasource to delete')
        delete_parser.add_argument('--workbook', default=None,
                                   help='name of workbook to delete')
        args = delete_parser.parse_args(sys.argv[DeleteParser.USER_ARG_IDX:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
