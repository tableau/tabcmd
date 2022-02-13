from .project_command import *
from .. import DeleteProjectParser
import tableauserverclient as TSC
from .. import log
from ... import Session
from ..commands import Commands


class DeleteProjectCommand(ProjectCommand):
    """
    Command to Delete the specified project from the server
    """
    @classmethod
    def parse(cls):
        args = DeleteProjectParser.delete_project_parser()
        return cls(args)

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        try:
            project_id = ProjectCommand.find_project_id(server, args.name)
        except ValueError as e:
            Commands.exit_with_error(
                logger,
                "Could not find project. Please check the name and try again")
        try:
            server.projects.delete(project_id)
            logger.info("Successfully deleted project")
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, "Server error occurred", e)
