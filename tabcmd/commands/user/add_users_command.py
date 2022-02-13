from .user_command import UserCommand
from .. import AddUserParser
import tableauserverclient as TSC
from .. import log
from ... import Session


class AddUserCommand(UserCommand):
    """
    Command to Adds users to a specified group
    """
    @classmethod
    def parse(cls):
        args = AddUserParser.add_user_parser()
        return cls(args)

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        number_of_users_added = 0
        number_of_errors = 0
        user_obj_list = UserCommand.get_users_from_file(args.csv_lines)
        for user_obj in user_obj_list:
            username = user_obj.username
            user_id = UserCommand.find_user_id(server, username)
            group = UserCommand.find_group(server, args.group_name)
            try:
                server.groups.add_user(group, user_id)
                number_of_users_added += 1
                logger.info("Successfully added")
            except TSC.ServerResponseError as e:
                logger.error("Error: Server error occurred", e)
                number_of_errors += 1
        logger.info("======== 100% complete ========")
        logger.info("======== Number of users added: {} =========".format(number_of_users_added))
        if number_of_errors > 0:
            logger.info("======== Number of errors {} =========".format(number_of_errors))