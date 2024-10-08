from tabcmd.commands.auth.session import Session
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .user_data import UserCommand


class RemoveUserCommand(UserCommand):
    """
    Command to remove users from the specified group
    """

    name: str = "removeusers"
    description: str = _("removeusers.short_description")

    @staticmethod
    def define_args(remove_users_parser):
        args_group = remove_users_parser.add_argument_group(title=RemoveUserCommand.name)
        args_group.add_argument("name", help="The group to remove users from.")
        set_users_file_arg(args_group)
        set_completeness_options(args_group)

    @classmethod
    def run_command(cls, args):
        logger = log(cls.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)

        logger.info(_("tabcmd.removeusers.server").format(args.users.name, args.name))

        UserCommand.act_on_users(logger, server, "removed", server.groups.remove_user, args)
