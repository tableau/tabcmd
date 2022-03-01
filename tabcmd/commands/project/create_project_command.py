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
        parent_id = None
        readable_name = args.name
        if args.parent_project_path is not None:
            try:
                logger.info("===== Identifying parent project '{}' on the server...".format(args.parent_project_path))
                parent = ProjectCommand.get_project_by_name_and_parent_path(server, None, args.parent_project_path)
            except TSC.ServerResponseError as exc:
                Commands.exit_with_error(logger, "Error fetching parent project", exc)
            readable_name = "{0}/{1}".format(args.parent_project_path, args.name)
            parent_id = parent.id
            logger.debug("parent project path = `{0}`, id = {1}".format(args.parent_project_path, parent_id))
        logger.info("===== Creating project '{}' on the server...".format(readable_name))
        new_project = TSC.ProjectItem(args.name, args.description, None, parent_id)
        try:
            project_item = server.projects.create(new_project)
            logger.info("===== Succeeded")
            return project_item
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, e)
