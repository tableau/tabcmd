from .project_command import *
from .. import PublishSamplesParser
import tableauserverclient as TSC
from .. import log
from ... import Session


class PublishSamplesCommand(ProjectCommand):
    """
    Command to Publish Tableau Sample workbooks to the specified project.
    Any existing samples will be overwritten.
    """

    def __init__(self, args, evaluated_project_path):
        super().__init__(args, evaluated_project_path)
        self.args = args
        self.logger = log('tabcmd.publish_samples_command',
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
