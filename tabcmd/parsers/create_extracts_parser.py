from .global_options import *


class CreateExtractsParser:
    """
    Parser for createextracts command
    """

    @staticmethod
    def create_extracts_parser(manager, command):
        """Method to parse create extracts arguments passed by the user"""
        create_extract_parser = manager.include(command)
        set_ds_xor_wb_args(create_extract_parser)
        set_embedded_datasources_options(create_extract_parser)
        set_encryption_option(create_extract_parser)
        set_project_arg(create_extract_parser)
        set_parent_project_arg(create_extract_parser)
        set_site_url_arg(create_extract_parser)
