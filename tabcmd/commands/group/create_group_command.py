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
    description: str = "tabcmd.command.description.create_group"

    @staticmethod
    def define_args(create_group_parser):
        create_group_parser.add_argument("name", help="tabcmd.command.arg.description.create_group.name")


    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug("tabcmd.launching")
        session = Session()
        server = session.create_session(args)
        try:
            logger.info(_("tabcmd.create.group").format(name=args.name))
            new_group = TSC.GroupItem(args.name)
            server.groups.create(new_group)
            logger.info(_("tabcmd.result.succeeded"))
        except TSC.ServerResponseError as e:
            if args.continue_if_exists and Errors.is_resource_conflict(e):
                logger.info(_("tabcmd.result.already_exists.group").format(args.name))
                return
            Errors.exit_with_error(logger, "tabcmd.result.failed.create_group")
