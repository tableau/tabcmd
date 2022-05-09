from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .user_data import UserCommand
from tabcmd import _


class RemoveUserCommand(UserCommand):
    """
    Command to remove users from the specified group
    """

    name: str = "removeusers"
    description: str = "tabcmd.command.description.remove_users"

    @staticmethod
    def define_args(remove_users_parser):
        remove_users_parser.add_argument(
            "name",
            help="tabcmd.command.description.remove_users.argument.name")
        set_users_file_arg(remove_users_parser)
        set_completeness_options(remove_users_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug("tabcmd.launching")
        session = Session()
        server = session.create_session(args)

        logger.info(_("tabcmd.delete.users.from_server").format(args.users.name, args.name))

        UserCommand.act_on_users(logger, server, "removed", server.groups.remove_user, args)
