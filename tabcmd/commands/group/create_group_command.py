import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log


class CreateGroupCommand(Server):
    """
    This command is used to create a group
    """

    name: str = "creategroup"
    description: str = "Create a local group"

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        try:
            logger.info("Creating group '{}' on the server...".format(args.name))
            new_group = TSC.GroupItem(args.name)
            server.groups.create(new_group)
            logger.info("Succeeded")
        except TSC.ServerResponseError as e:
            Server.exit_with_error(logger, "Error while communicating with the server")
