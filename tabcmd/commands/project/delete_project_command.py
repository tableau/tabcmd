from ..commands import Commands
from .project_command import *
from .. import DeleteProjectParser
import tableauserverclient as TSC
from .. import log
from ... import Session


class DeleteProjectCommand(ProjectCommand):
    """
    Command to Delete the specified project from the server
    """
    def __init__(self, args, evaluated_project_path):
        super().__init__(args, evaluated_project_path)
        self.logger = log('tabcmd.delete_project_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        args, evaluated_project_path = \
            DeleteProjectParser.delete_project_parser()
        return cls(args, evaluated_project_path)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.delete_project(server_object)

    def delete_project(self, server):
        """Method to delete project using Tableauserverclient methods"""
        try:
            project_id = ProjectCommand.find_project_id(server, self.name)
            server.projects.delete(project_id)
            self.logger.info("Successfully deleted project")
        except TSC.ServerResponseError as e:
            self.logger.error("Server error occurred", e)
        except ValueError as e:
            self.logger.error("Project does not exist")
