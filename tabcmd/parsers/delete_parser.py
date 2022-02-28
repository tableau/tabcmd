from .global_options import *


class DeleteParser:
    """Parser for the command delete"""

    @staticmethod
    def delete_parser(manager, command):
        """Method to parse delete data source arguments passed by the user"""

        delete_parser = manager.include(command)
        delete_parser_group = delete_parser.add_mutually_exclusive_group(required=True)
        delete_parser_group.add_argument(
            "name", nargs="?", help="The datasource or workbook to delete"
        )
        delete_parser_group.add_argument(
            "--workbook", required=False, help="The workbook to delete"
        )
        delete_parser_group.add_argument(
            "--datasource", required=False, help="The datasource to delete"
        )
        set_project_r_arg(delete_parser)
