from .global_options import *


class PublishParser:
    """Parser to the command publish"""

    @staticmethod
    def publish_parser(manager, command):
        """Method to parse publish arguments passed by the user"""
        publish_parser = manager.include(command)
        publish_parser.add_argument('filename')
        set_publish_args(publish_parser)
        set_project_r_arg(publish_parser)
        set_parent_project_arg(publish_parser)
