from src.commands.auth.session import Session
from src.commands.constants import Errors
from src.commands.server import Server
from src.execution.global_options import *
from src.execution.localize import _
from src.execution.logger_config import log


class PublishSamplesCommand(Server):
    """
    Command to Publish Tableau Sample workbooks to the specified project.
    Any existing samples will be overwritten.
    """

    name: str = "publishsamples"
    description: str = _("publishsamples.short_description")

    @staticmethod
    def define_args(publish_samples_parser):
        publish_samples_parser.add_argument(
            "--name",
            "-n",
            dest="project_name",
            required=True,
        )
        set_parent_project_arg(publish_samples_parser)  # args.parent_project_name

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
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
            Errors.exit_with_error(logger, _("tabcmd.report.error.publish_samples.expected_project"), exception=e)

        try:
            server.projects.update(project, samples=True)
        except Exception as e:
            Errors.exit_with_error(logger, _("tabcmd.result.failure.publish_samples"), exception=e)
