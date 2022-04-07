import tableauserverclient as TSC

from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log


class CreateProjectCommand(Server):
    """
    Command to create a project
    """

    name: str = "createproject"
    description: str = "Create a project"

    @staticmethod
    def define_args(create_project_parser):
        create_project_parser.add_argument("--name", "-n", dest="project_name", required=True, help="name of project")
        set_parent_project_arg(create_project_parser)
        set_description_arg(create_project_parser)

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        parent_id = None
        readable_name = args.project_name
        if args.parent_project_path is not None:
            try:
                logger.info("===== Identifying parent project '{}' on the server...".format(args.parent_project_path))
                parent = Server.get_project_by_name_and_parent_path(logger, server, None, args.parent_project_path)
            except TSC.ServerResponseError as exc:
                Errors.exit_with_error(logger, "Error fetching parent project", exc)
            readable_name = "{0}/{1}".format(args.parent_project_path, args.project_name)
            parent_id = parent.id
            logger.debug("parent project path = `{0}`, id = {1}".format(args.parent_project_path, parent_id))
        logger.info("===== Creating project '{}' on the server...".format(readable_name))
        new_project = TSC.ProjectItem(args.project_name, args.description, None, parent_id)
        try:
            project_item = server.projects.create(new_project)
            logger.info("===== Succeeded")
            return project_item
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Error creating project", e)
