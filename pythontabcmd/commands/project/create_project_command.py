from .project_command import *
from .. import CreateProjectParser
import tableauserverclient as TSC
from .. import log
from ..auth.login_command import LoginCommand
from ... import Session


class CreateProjectCommand(ProjectCommand):
    """
    Command to create a project
    """
    def __init__(self, args, evaluated_project_path):
        super().__init__(args, evaluated_project_path)
        self.args = args
        self.description = args.description
        self.content_permission = args.content_permission
        self.logger = log('pythontabcmd.create_project_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args, evaluated_project_path = \
            CreateProjectParser.create_project_parser()
        return cls(args, evaluated_project_path)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.create_project(server_object)

    def create_project(self, server):
        """Method to create project using tableauserverclient methods"""
        if self.parent_path_name is not None:
            project_path = ProjectCommand. \
                find_project_id(server, self.parent_path_name)
        else:
            project_path = None
        top_level_project = \
            TSC.ProjectItem(self.name, self.description,
                            self.content_permission, project_path)
        self.create_project_helper(server, top_level_project)

    def create_project_helper(self, server, project_item):
        """ Helper method to catch server errors
        thrown by tableauserverclient"""

        try:
            project_item = server.projects.create(project_item)
            self.logger.info('Successfully created a new '
                             'project called: %s'
                             % project_item.name)
            return project_item
        except TSC.ServerResponseError as e:
            self.logger.error('We have already created '
                              'this project: %s'
                              % project_item.name)
