import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log


class DeleteGroupCommand(Server):
    """
    This command deletes the specified group from the server
    """

    name: str = "deletegroup"
    description: str = "Delete a group"

    @staticmethod
    def define_args(delete_group_parser):
        delete_group_parser.add_argument("name", help="name of group to delete")

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        try:
            logger.info("Finding group {} on server...".format(args.name))
            group_id = Server.find_group_id(logger, server, args.name)
            logger.info("Deleting group {} on server...".format(group_id))
            server.groups.delete(group_id)
            logger.info("===== Succeeded")
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Error deleting group from server", e)
