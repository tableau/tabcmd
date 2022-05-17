import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log
from tabcmd.commands.constants import Errors
from tabcmd.execution.localize import _


class DeleteGroupCommand(Server):
    """
    This command deletes the specified group from the server
    """

    name: str = "deletegroup"
    description: str = _("deletegroup.short_description")

    @staticmethod
    def define_args(delete_group_parser):
        delete_group_parser.add_argument("name")

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        try:
            logger.info(_("tabcmd.find.group").format(args.name))
            group_id = Server.find_group_id(logger, server, args.name)
            logger.info(_("deletegroup.status").format(group_id))
            server.groups.delete(group_id)
            logger.info(_("tabcmd.result.succeeded"))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "tabcmd.result.failed.delete.group", e)
