from .project_command import *
from ..auth.session import Session
from ..commands import Commands
from tabcmd.parsers.create_project_parser import CreateProjectParser
import tableauserverclient as TSC
from tabcmd.execution.logger_config import log


class CreateProjectCommand(ProjectCommand):
    """
    Command to create a project
    """

    @classmethod
    def parse(cls):
        args = CreateProjectParser.create_project_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        if args.parent_project_path is not None:
            project_path = ProjectCommand.find_project_id(
                server, args.parent_project_path
            )
        else:
            project_path = None

        logger.info("===== Creating project '{}' on the server...".format(args.name))
        top_level_project = TSC.ProjectItem(
            args.name, args.description, None, project_path
        )
        try:
            project_item = server.projects.create(top_level_project)
            logger.info("===== Succeeded")
            return project_item
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, "Error", e)
