from .global_options import *


class PublishSamplesParser:
    """
    Parser to the command publishsamples
    """

    @staticmethod
    def publish_samples_parser(manager, command):
        """Method to parse publish samples arguments passed by the user"""
        publish_samples_parser = manager.include(command)
        publish_samples_parser.add_argument(
            "--name",
            "-n",
            dest="project_name",
            required=True,
            help="Publishes the Tableau samples into the specified project. If the project name includes spaces, "
            "enclose the entire name in quotes.",
        )
        set_parent_project_arg(publish_samples_parser)
