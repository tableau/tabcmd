import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log
from tabcmd.commands.constants import Errors
from tabcmd import _


class CreateGroupCommand(Server):
    """
    This command is used to create a group
    """
    name: str = "creategroup"
    description: str = "Create a local group"

    @staticmethod
    def define_args(create_group_parser):
        create_group_parser.add_argument("name")

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        print(_("HelloHelloWorld"))
        logger.debug(_("======================= Launching command ======================="))
        logger.info(_("helloworld"))
        session = Session()
        server = session.create_session(args)
        try:
            logger.info("Creating group '{}' on the server...".format(args.name))
            new_group = TSC.GroupItem(args.name)
            server.groups.create(new_group)
            logger.info(_("Succeeded"))
        except TSC.ServerResponseError as e:
            if args.continue_if_exists and Errors.is_resource_conflict(e):
                logger.info(_("Group called {} already exists".format(args.name)))
                return
            Errors.exit_with_error(logger, "Error while communicating with the server")
