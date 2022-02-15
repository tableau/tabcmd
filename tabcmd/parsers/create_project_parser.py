from .global_options import *


class CreateProjectParser:
    """
    Parser for createproject command
    """

    @staticmethod
    def create_project_parser(manager, command):
        """Method to parse create project arguments passed by the user"""

        create_project_parser = manager.include(command)
        create_project_parser.add_argument('--name', '-n', required=True, help='name of project')
        set_parent_project_arg(create_project_parser)
        set_description_arg(create_project_parser)
