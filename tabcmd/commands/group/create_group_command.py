import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class CreateGroupCommand(Server):
    """
    This command is used to create a group
    """

    name: str = "creategroup"
    description: str = _("creategroup.short_description")

    @staticmethod
    def define_args(create_group_parser):
        args_group = create_group_parser.add_argument_group(title=CreateGroupCommand.name)
        args_group.add_argument("name")

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
        except Exception as e:
            if args.continue_if_exists and Errors.is_resource_conflict(e):
                logger.info(_("tabcmd.result.already_exists").format(_("content_type.group"), args.name))
                return
            Errors.exit_with_error(logger, _("tabcmd.result.failed.create_group"))
