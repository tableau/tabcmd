from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .project_command import *


class DeleteProjectCommand(ProjectCommand):
    """
    Command to Delete the specified project from the server
    """

    name: str = "deleteproject"
    description: str = "Delete a project"

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        if args.parent_project_path:
            logger.debug("parent path: {}".format(args.parent_project_path))

        try:
            logger.debug("Fetching project to be deleted: {}/{}".format(args.parent_project_path, args.project_name))
            project = ProjectCommand.get_project_by_name_and_parent_path(
                logger, server, args.project_name, args.parent_project_path
            )
        except TSC.ServerResponseError as e:
            Server.exit_with_error(logger, "Error finding project", e)
        project_id = project.id

        try:
            logger.info("Deleting project '{}' from the server...".format(args.project_name))
            server.projects.delete(project_id)
            logger.info("===== Succeeded")
        except TSC.ServerResponseError as e:
            Server.exit_with_error(logger, "Failed to delete project", e)
