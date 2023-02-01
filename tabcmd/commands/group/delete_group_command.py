import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class DeleteGroupCommand(Server):
    """
    This command deletes the specified group from the server
    """

    name: str = "deletegroup"
    description: str = _("deletegroup.short_description")

    @staticmethod
    def define_args(delete_group_parser):
        args_group = delete_group_parser.add_argument_group(title=DeleteGroupCommand.name)
        args_group.add_argument("name")

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)
        try:
            logger.info(_("tabcmd.find.group").format(args.name))
            group_id = Server.find_group(logger, server, args.name).id
            logger.info(_("deletegroup.status").format(group_id))
            server.groups.delete(group_id)
            logger.info(_("common.output.succeeded"))
        except Exception as e:
            Errors.exit_with_error(logger, _("tabcmd.result.failed.delete.group"), e)
