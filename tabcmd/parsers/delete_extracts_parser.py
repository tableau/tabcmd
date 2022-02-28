from .global_options import *


class DeleteExtractsParser:
    """
    Parser for the command delete extracts
    """

    @staticmethod
    def delete_extracts_parser(manager, command):
        """Method to parse delete extracts arguments passed by the user"""

        delete_extract_parser = manager.include(command)
        set_ds_xor_wb_args(delete_extract_parser)
        set_embedded_datasources_options(delete_extract_parser)
        # set_encryption_option(delete_extract_parser)
        set_project_arg(delete_extract_parser)
        set_parent_project_arg(delete_extract_parser)
        delete_extract_parser.add_argument("--url", help="The canonical name for the resource as it appears in the URL")
