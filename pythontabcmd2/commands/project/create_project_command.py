from .project_command import *
from .. import CreateProjectParser
import tableauserverclient as TSC
from .. import get_logger
from ..auth.login_command import LoginCommand
from ... import Session


class CreateProjectCommand(ProjectCommand):

    def __init__(self, args, evaluated_project_path):
        super().__init__(args, evaluated_project_path)
        self.args = args
        self.description = args.description
        self.content_permission = args.content_permission

    def log(self):
        logger = get_logger('pythontabcmd2.create_project_command',
                            self.logging_level)
        return logger

    @classmethod
    def parse(cls):
        args, evaluated_project_path = \
            CreateProjectParser.create_project_parser()
        return cls(args, evaluated_project_path)

    def run_command(self):
        if self.args.cookie and self.args.username:
            session = Session(self.args)
            session.username_password_authentication_with_token_save()
            server_object = Commands.deserialize()
            self.create_project(server_object)

        elif self.args.cookie and self.args.token_name:
            session = Session(self.args)
            session.personal_access_token_authentication_with_token_save()
            server_object = Commands.deserialize()
            self.create_project(server_object)
        elif self.args.no_cookie and self.args.username:
            session = Session(self.args)
            auth_token, site_id = session \
                .no_cookie_save_session_creation_with_username()
            server_object = session.no_cookie_server_object_creation(
                auth_token, site_id)
            self.create_project(server_object)

        elif self.args.no_cookie and self.args.token_name:
            print("ran this elif code black token no cookie")
            session = Session(self.args)
            auth_token, site_id = session \
                .no_cookie_save_session_creation_with_token()
            server_object = session.no_cookie_server_object_creation(
                auth_token, site_id)
            self.create_project(server_object)
        else:
            print("ran this else code block")
            server_object = Commands.deserialize()
            self.create_project(server_object)



    def create_project(self, server):
        """Method to create project using tableauserverclient methods"""
        project_path = ProjectCommand. \
            find_project_id(server, self.parent_path_name)
        top_level_project = \
            TSC.ProjectItem(self.name, self.description,
                            self.content_permission, project_path)
        top_level_project = self.create_project_helper(server,
                                                       top_level_project)

    def create_project_helper(self, server, project_item):
        """ Helper method to catch server errors
        thrown by tableauserverclient"""
        logger = self.log()
        try:
            project_item = server.projects.create(project_item)
            logger.info('Successfully created a new '
                        'project called: %s'
                        % project_item.name)
            return project_item
        except TSC.ServerResponseError as e:
            logger.error('We have already created '
                         'this project: %s'
                         % project_item.name)
