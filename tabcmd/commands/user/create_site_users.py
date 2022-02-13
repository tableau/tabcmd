from .. import Constants
from .user_command import UserCommand
from .. import CreateSiteUsersParser
import tableauserverclient as TSC
from .. import log
from ... import Session


class CreateSiteUsersCommand(UserCommand):
    """
    Command to add users to a site, based on information supplied in a comma-separated values (CSV) file.
    If the user is not already created on the server, the command creates the user before adding
    that user to the site
    """
    @classmethod
    def parse(cls):
        args = CreateSiteUsersParser.create_site_user_parser()
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
        logger.info("======== 0% complete ========")
        for user_obj in user_obj_list:
            username = user_obj.username
            try:
                new_user = TSC.UserItem(username, args.role)
                server.users.add(new_user)
                logger.info("Successfully created user: {}".format(username))
                number_of_users_added += 1
            except TSC.ServerResponseError as e:
                number_of_errors += 1
                if e.code == Constants.forbidden:
                    logger.error("User is not local, and the user's credentials are not maintained on Tableau Server.")
                if e.code == Constants.invalid_credentials:
                    logger.error("Unauthorized access, Please login")
                if e.code == Constants.user_already_member_of_site:
                    logger.error("User: {} already member of site".format(username))
        logger.info("======== 100% complete ========")
        logger.info("======== Number of users added: {} =========".
                         format(number_of_users_added))
        if number_of_errors > 0:
            logger.info("======== Number of errors {} =========".format(number_of_errors))
