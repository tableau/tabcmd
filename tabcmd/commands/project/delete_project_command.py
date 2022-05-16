import tableauserverclient as TSC

from tabcmd.commands.constants import Errors
from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log
from tabcmd import _


class DeleteProjectCommand(Server):
    """
    Command to Delete the specified project from the server
    """

    name: str = "deleteproject"
    description: str = "tabcmd.help.command.deleteproject"

    @staticmethod
    def define_args(delete_project_parser):
        delete_project_parser.add_argument("project_name", metavar="project-name", help="name of project to delete")
        set_parent_project_arg(delete_project_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        if args.parent_project_path:
            logger.debug("parent path: {}".format(args.parent_project_path))

        try:
            logger.debug("tabcmd.find.project".format(args.parent_project_path, args.project_name))
            project = Server.get_project_by_name_and_parent_path(
                logger, server, args.project_name, args.parent_project_path
            )
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "tabcmd.result.failure.find.project", e)
        project_id = project.id

        try:
            logger.info(_("tabcmd.delete.project").format(args.project_name))
            server.projects.delete(project_id)
            logger.info(_("tabcmd.succeeded"))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "tabcmd.result.failure.delete.project", e)
