from tabcmd.parsers.remove_users_parser import RemoveUserParser
from .user_command import UserCommand
import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from ..auth.session import Session


class RemoveUserCommand(UserCommand):
    """
     Command to remove users from the specified group
    """
    @classmethod
    def parse(cls):
        args = RemoveUserParser.remove_user_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        number_of_users_removed = 0
        number_of_errors = 0
        user_obj_list = UserCommand.get_users_from_file(args.csv_lines)
        for user_obj in user_obj_list:
            username = user_obj.username
            user_id = UserCommand.find_user_id(server, username)
            group = UserCommand.find_group(server, args.group_name)
            try:
                server.groups.remove_user(group, user_id)
                number_of_users_removed += 1
                logger.info("Successfully removed {0} from {1}".format(user_obj.username, args.group_name))
            except TSC.ServerResponseError as e:
                logger.error("Error: Server error occurred", e)
                number_of_errors += 1
                # TODO Map Error code
        logger.info("======== 100% complete ========")
        logger.info("======== Number of users removed: {} =========".format(number_of_users_removed))
        if number_of_errors > 0:
            logger.info("======== Number of errors {} =========".format(number_of_errors))