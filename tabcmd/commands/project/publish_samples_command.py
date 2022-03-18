from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log


class PublishSamplesCommand(Server):
    """
    Command to Publish Tableau Sample workbooks to the specified project.
    Any existing samples will be overwritten.
    """

    name: str = "publishsamples"
    description: str = "Publish samples to the server"

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        if args.parent_path_name is not None:
            project_path = Server.find_project_id(server, args.parent_path_name)
        else:
            project_path = None
        Server.exit_with_error(logger, "Not yet implemented")
