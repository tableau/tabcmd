from commands.commands import Commands
from commands.project.project_command import ProjectCommand
from parsers.create_project_parser import CreateProjectParser
from .project_command import *

try:
    from tabcmd2.pythontabcmd2 import tableauserverclient as TSC
    from logger_config import get_logger
except:
    import tableauserverclient as TSC
    from logger_config import get_logger
logger = get_logger('pythontabcmd2.create_project_command')


class CreateProjectCommand(ProjectCommand):
    def __init__(self, args, evaluated_project_path):
        super().__init__(args, evaluated_project_path)
        self.description = args.description
        self.content_permission = args.content_permission

    @classmethod
    def parse(cls):
        args, evaluated_project_path = CreateProjectParser.create_project_parser()
        return cls(args, evaluated_project_path)

    def run_command(self):
        signed_in_object, server_object = Commands.deserialize()
        self.create_project(server_object)

    def create_project(self, newserver):
        """Method to create project using tableauserverclient methods"""
        project_path = ProjectCommand.find_project_id(newserver, self.parent_path_name)
        top_level_project = TSC.ProjectItem(self.name, self.description, self.content_permission, project_path)
        top_level_project = self.create_project_helper(newserver, top_level_project)

    def create_project_helper(self, server, project_item):
        """ Helper method to catch server errors thrown by tableauserverclient"""
        try:
            project_item = server.projects.create(project_item)
            logger.info('Successfully created a new project called: %s' % project_item.name)
            return project_item
        except TSC.ServerResponseError as e:
            logger.info('Error: We have already created this project: %s' % project_item.name)

