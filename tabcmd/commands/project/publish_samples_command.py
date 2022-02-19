from .project_command import *
from tabcmd.parsers.publish_samples_parser import PublishSamplesParser
from tabcmd.execution.logger_config import log
from ..auth.session import Session
from ..commands import Commands


class PublishSamplesCommand(ProjectCommand):
    """
    Command to Publish Tableau Sample workbooks to the specified project.
    Any existing samples will be overwritten.
    """
    @classmethod
    def parse(cls):
        args = PublishSamplesParser.publish_samples_parser()
        return args

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
        Commands.exit_with_error(logger, "Not yet implemented")
