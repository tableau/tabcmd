import tableauserverclient as TSC

from src.commands.auth.session import Session
from src.commands.constants import Errors
from src.commands.server import Server
from src.execution.localize import _
from src.execution.logger_config import log


class CreateGroupCommand(Server):
    """
    This command is used to create a group
    """

    name: str = "creategroup"
    description: str = _("creategroup.short_description")

    @staticmethod
    def define_args(create_group_parser):
        create_group_parser.add_argument("name")

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        try:
            logger.info(_("creategroup.status").format(args.name))
            new_group = TSC.GroupItem(args.name)
            server.groups.create(new_group)
            logger.info(_("common.output.succeeded"))
        except TSC.ServerResponseError as e:
            # quite likely a 403 because you must be server/site admin to call this
            if args.continue_if_exists and Errors.is_resource_conflict(e):
                logger.info(_("tabcmd.result.already_exists.group").format(args.name))
                return
            Errors.exit_with_error(logger, _("tabcmd.result.failed.create_group"))
