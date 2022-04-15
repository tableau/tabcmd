from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log
from tabcmd.commands.constants import Errors


class PublishSamplesCommand(Server):
    """
    Command to Publish Tableau Sample workbooks to the specified project.
    Any existing samples will be overwritten.
    """

    name: str = "publishsamples"
    description: str = "Publish samples to the server"

    @staticmethod
    def define_args(publish_samples_parser):
        publish_samples_parser.add_argument(
            "--name",
            "-n",
            dest="project_name",
            required=True,
            help="Publishes the Tableau samples into the specified project. If the project name includes spaces, "
            "enclose the entire name in quotes.",
        )
        set_parent_project_arg(publish_samples_parser)  # args.parent_project_name

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        if args.parent_project_path is not None:
            project_path = Server.get_project_by_name_and_parent_path(logger, server, None, args.parent_project_path)
        else:
            project_path = None
        try:
            project = PublishSamplesCommand.get_project_by_name_and_parent_path(
                logger, server, args.project_name, project_path
            )
        except Exception as e:
            Errors.exit_with_error(logger, "publishsamples expects the specified project to exist already", exception=e)

        try:
            server.projects.update(project, samples=True)
        except Exception as e:
            Errors.exit_with_error(logger, "Failed publishing samples to project", exception=e)
