import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class DeleteProjectCommand(Server):
    """
    Command to Delete the specified project from the server
    """

    name: str = "deleteproject"
    description: str = _("deleteproject.short_description")

    @staticmethod
    def define_args(delete_project_parser):
        args_group = delete_project_parser.add_argument_group(title=DeleteProjectCommand.name)
        args_group.add_argument("project_name", metavar="project-name", help=_("createproject.options.name"))
        set_parent_project_arg(args_group)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        if args.parent_project_path:
            logger.debug("parent path: {}".format(args.parent_project_path))

        try:
            logger.debug(_("deleteproject.status").format(args.parent_project_path, args.project_name))
            project = Server.get_project_by_name_and_parent_path(
                logger, server, args.project_name, args.parent_project_path
            )
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response"), e)
        project_id = project.id

        try:
            logger.info(_("deleteproject.status").format(args.project_name))
            server.projects.delete(project_id)
            logger.info(_("common.output.succeeded"))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "tabcmd.result.failure.delete.project", e)
