import tableauserverclient as TSC

from tabcmd.commands.constants import Errors
from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .user_data import UserCommand


class AddUserCommand(UserCommand):
    """
    Command to Adds users to a specified group
    """

    name: str = "addusers"
    description: str = "Add users to a group"

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        number_of_users_listed = 0
        number_of_users_added = 0
        number_of_errors = 0
        if args.require_all_valid:
            number_of_users_listed = UserCommand.validate_file_for_import(args.users, logger)
        logger.info("Adding users listed in {0} to group '{1}'".format(args.users.name, args.name))
        user_obj_list = UserCommand.get_users_from_file(args.users)
        for user_obj in user_obj_list:
            username = user_obj.username
            user_id = UserCommand.find_user_id(logger, server, username)
            group = UserCommand.find_group(logger, server, args.name)
            try:
                number_of_users_listed += 1
                server.groups.add_user(group, user_id)
                number_of_users_added += 1
                logger.info("Successfully added")
            except TSC.ServerResponseError as e:
                Errors.check_common_error_codes(logger.info(), e)
                number_of_errors += 1
        if number_of_users_added == 0:
            logger.info("File does not contain any valid usernames")
            return

        logger.info("======== 100% complete ========")
        logger.info("======== Number of users listed: {} =========".format(number_of_users_listed))
        logger.info("======== Number of users added: {} =========".format(number_of_users_added))
        if number_of_errors > 0:
            logger.info("======== Number of errors {} =========".format(number_of_errors))
