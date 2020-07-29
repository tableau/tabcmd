from ..commands import Commands
from .project_command import *
from .. import DeleteProjectParser
import tableauserverclient as TSC
from .. import get_logger

logger = get_logger('pythontabcmd2.delete_project_command')


class DeleteProjectCommand(ProjectCommand):
    def __init__(self, args, evaluated_project_path):
        super().__init__(args, evaluated_project_path)

    @classmethod
    def parse(cls):
        args, evaluated_project_path = \
            DeleteProjectParser.delete_project_parser()
        return cls(args, evaluated_project_path)

    def run_command(self):
        signed_in_object, server_object = Commands.deserialize()
        self.delete_project(server_object)

    def delete_project(self, server):
        """Method to delete project using Tableauserverclient methods"""
        try:
            project_id = ProjectCommand.find_project_id(server, self.name)
            server.projects.delete(project_id)
            logger.info("Successfully deleted project")
        except TSC.ServerResponseError as e:
            logger.info("Error: Server error occured", e)
            # TODO ERROR
