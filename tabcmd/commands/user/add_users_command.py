import tableauserverclient as TSC

from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.execution.logger_config import log
from .user_data import UserCommand
from tabcmd import _


class AddUserCommand(UserCommand):
    """
    Command to Adds users to a specified group
    """

    name: str = "addusers"
    description: str = "Add users to a group"

    @staticmethod
    def define_args(add_user_parser):
        add_user_parser.add_argument("name", help="name of group to add users to")
        set_users_file_arg(add_user_parser)
        set_completeness_options(add_user_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)

        logger.info(_("Adding users listed in {0} to group '{1}'").format(args.users.name, args.name))

        UserCommand.act_on_users(logger, server, "added", server.groups.add_user, args)
