import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .project_command import *


class CreateProjectCommand(ProjectCommand):
    """
    Command to create a project
    """

    name: str = "createproject"
    description: str = "Create a project"

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
                parent = ProjectCommand.get_project_by_name_and_parent_path(
                    logger, server, None, args.parent_project_path
                )
            except TSC.ServerResponseError as exc:
                Server.exit_with_error(logger, "Error fetching parent project", exc)
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
            Server.exit_with_error(logger, "Error creating project", e)
