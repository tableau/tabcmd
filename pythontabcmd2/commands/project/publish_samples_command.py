from .project_command import *
from .. import PublishSamplesParser
import tableauserverclient as TSC
from .. import log
from ... import Session


class PublishSamplesCommand(ProjectCommand):

    def __init__(self, args, evaluated_project_path):
        super().__init__(args, evaluated_project_path)
        self.args = args
        self.logger = log('pythontabcmd2.publish_samples_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args, evaluated_project_path = \
            PublishSamplesParser.publish_samples_parser()
        return cls(args, evaluated_project_path)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.publish_samples(server_object)

    def publish_samples(self, server):
        """Method to publish samples using tableauserverclient methods"""
        if self.parent_path_name is not None:
            project_path = ProjectCommand. \
                find_project_id(server, self.parent_path_name)
        else:
            project_path = None

        #check is self.username is none:
                # check if json present
                    #yes -> get username/password
                #no: login again



        # top_level_project = \
        #     TSC.ProjectItem(self.name, self.description,
        #                     self.content_permission, project_path)
    #     self.create_project_helper(server, top_level_project)
    #
    # def create_project_helper(self, server, project_item):
    #     """ Helper method to catch server errors
    #     thrown by tableauserverclient"""
    #
    #     try:
    #         project_item = server.projects.create(project_item)
    #         self.logger.info('Successfully created a new '
    #                          'project called: %s'
    #                          % project_item.name)
    #         return project_item
    #     except TSC.ServerResponseError as e:
    #         self.logger.error('We have already created '
    #                           'this project: %s'
    #                           % project_item.name)
