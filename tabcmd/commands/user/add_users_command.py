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

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)

        logger.info(_("tabcmd.add.users.to_site").format(args.users.name, args.name))

        UserCommand.act_on_users(logger, server, "added", server.groups.add_user, args)
