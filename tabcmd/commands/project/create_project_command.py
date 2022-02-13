from .project_command import *
from .. import CreateProjectParser
import tableauserverclient as TSC
from .. import log
from ... import Session
from ..commands import Commands


class CreateProjectCommand(ProjectCommand):
    """
    Command to create a project
    """
    @classmethod
    def parse(cls):
        args = CreateProjectParser.create_project_parser()
        return cls(args)

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        if args.parent_path_name is not None:
            project_path = ProjectCommand.find_project_id(server, args.parent_path_name)
        else:
            project_path = None

        top_level_project = TSC.ProjectItem(args.project_name, args.description, args.content_permission,
                                            project_path)
        try:
            project_item = server.projects.create(top_level_project)
            logger.info('Successfully created a new project called: ', top_level_project.name)
            return project_item
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, 'A project by this name already exists', e)
