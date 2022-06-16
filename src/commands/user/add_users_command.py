from src.commands.auth.session import Session
from src.execution.global_options import *
from src.execution.localize import _
from src.execution.logger_config import log
from .user_data import UserCommand


class AddUserCommand(UserCommand):
    """
    Command to Adds users to a specified group
    """

    name: str = "addusers"
    description: str = _("addusers.short_description")

    @staticmethod
    def define_args(add_user_parser):
        add_user_parser.add_argument("name", help="name of group to add users to")
        set_users_file_arg(add_user_parser)
        set_completeness_options(add_user_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)

        logger.info(_("tabcmd.add.users.to_site").format(args.users.name, args.name))

        UserCommand.act_on_users(logger, server, "added", server.groups.add_user, args)
