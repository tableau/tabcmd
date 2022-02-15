from .global_options import *


class DeleteParser:
    """Parser for the command delete"""

    @staticmethod
    def delete_parser(manager, command):
        """Method to parse delete data source arguments passed by the user"""

        delete_parser = manager.include(command)
        delete_parser.add_argument('name', help='The datasource or workbook to delete')
        set_project_r_arg(delete_parser)

