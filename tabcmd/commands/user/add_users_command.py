from tabcmd.commands.auth.session import Session
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .user_data import UserCommand


class AddUserCommand(UserCommand):
    """
    Command to Adds users to a specified group
    """

    name: str = "addusers"
    description: str = _("addusers.short_description")

    @staticmethod
    def define_args(add_user_parser):
        args_group = add_user_parser.add_argument_group(title=AddUserCommand.name)
        args_group.add_argument("name", help="name of group to add users to")
        set_users_file_arg(args_group)
        set_completeness_options(args_group)

    @classmethod
    def run_command(cls, args):
        logger = log(cls.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)

        logger.info(_("addusers.status").format(args.users.name, args.name))

        UserCommand.act_on_users(logger, server, "added", server.groups.add_user, args)
