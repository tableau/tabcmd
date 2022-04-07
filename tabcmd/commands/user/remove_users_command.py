from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .user_data import UserCommand


class RemoveUserCommand(UserCommand):
    """
    Command to remove users from the specified group
    """

    name: str = "removeusers"
    description: str = "Remove users from a group"

    @staticmethod
    def define_args(remove_users_parser):
        remove_users_parser.add_argument("name", help="The group to remove users from.")
        set_users_file_arg(remove_users_parser)
        set_completeness_options(remove_users_parser)

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)

        logger.info("Removing users listed in {0} from group '{1}'".format(args.users.name, args.name))

        UserCommand.act_on_users(logger, server, "removed", server.groups.remove_user, args)
