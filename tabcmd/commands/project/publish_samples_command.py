from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class PublishSamplesCommand(Server):
    """
    Command to Publish Tableau Sample workbooks to the specified project.
    Any existing samples will be overwritten.
    """

    name: str = "publishsamples"
    description: str = _("publishsamples.short_description")

    @staticmethod
    def define_args(publish_samples_parser):
        args_group = publish_samples_parser.add_argument_group(title=PublishSamplesCommand.name)
        args_group.add_argument(
            "--name",
            "-n",
            dest="project_name",
            required=True,
        )
        set_parent_project_arg(args_group)  # args.parent_project_name

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)
        try:
            project = PublishSamplesCommand.get_project_by_name_and_parent_path(
                logger, server, args.project_name, args.parent_project_path
            )
        except Exception as e:
            Errors.exit_with_error(logger, _("tabcmd.report.error.publish_samples.expected_project"), exception=e)

        try:
            server.projects.update(project, samples=True)
        except Exception as e:
            Errors.exit_with_error(logger, _("tabcmd.result.failure.publish_samples"), exception=e)
