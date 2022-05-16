import tableauserverclient as TSC

from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log
from tabcmd.commands.constants import Errors
from tabcmd import _


class CreateProjectCommand(Server):
    """
    Command to create a project
    """

    name: str = "createproject"
    description: str = "tabcmd.command.description.create_project"

    @staticmethod
    def define_args(create_project_parser):
        create_project_parser.add_argument("--name", "-n", dest="project_name", required=True,
                                           help="tabcmd.command.arg.description.create_project.name")
        set_parent_project_arg(create_project_parser)
        set_description_arg(create_project_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        parent_id = None
        readable_name = args.project_name
        if args.parent_project_path:
            try:
                logger.info("tabcmd.find.parent_project".format(args.parent_project_path))
                parent = Server.get_project_by_name_and_parent_path(logger, server, None, args.parent_project_path)
            except TSC.ServerResponseError as exc:
                Errors.exit_with_error(logger, "tabcmd.result.failed.find.parent_project", exc)
            readable_name = "{0}/{1}".format(args.parent_project_path, args.project_name)
            parent_id = parent.id
            logger.debug("parent project = `{0}`, id = {1}".format(args.parent_project_path, parent_id))
        logger.info(_("tabcmd.create.project").format(readable_name))
        new_project = TSC.ProjectItem(args.project_name, args.description, None, parent_id)
        try:
            project_item = server.projects.create(new_project)
            logger.info(_("tabcmd.succeeded"))
            return project_item
        except TSC.ServerResponseError as e:
            if args.continue_if_exists and Errors.is_resource_conflict(e):
                logger.info("tabcmd.result.already_exists".format(args.project_name))
                return
            Errors.exit_with_error(logger, "tabcmd.result.failed.createproject", e)
