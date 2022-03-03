from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .project_command import *


class DeleteProjectCommand(ProjectCommand):
    """
    Command to Delete the specified project from the server
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        try:
            project_id = ProjectCommand.find_project_id(server, args.name)
        except ValueError as e:
            Commands.exit_with_error(logger, "Could not find project. Please check the name and try again")
        try:
            logger.info("Deleting project '{}' from the server...".format(args.name))
            server.projects.delete(project_id)
            logger.info("Succeeded")
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, "Server error occurred", e)
