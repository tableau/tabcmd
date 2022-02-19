from ..user.user_command import UserCommand
import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from ..auth.session import Session
from .site_command import SiteCommand
from tabcmd.parsers.delete_site_users_parser import DeleteSiteUsersParser


class DeleteSiteUsersCommand(SiteCommand):
    """
    Command to Remove users from the site that user is logged in to.
    The users to be removed are specified in a file that contains
    a simple list of one user name per line.
    """
    @classmethod
    def parse(cls):
        args = DeleteSiteUsersParser.delete_site_users_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)

        number_of_users_deleted = 0
        number_of_errors = 0
        user_obj_list = UserCommand.get_users_from_file(args.csv_lines)
        logger.info("======== 0% complete ========")
        for user_obj in user_obj_list:
            username = user_obj.username
            user_id = UserCommand.find_user_id(server, username)
            try:
                server.users.remove(user_id)
                logger.info("Successfully deleted user from site: {}".format(username))
                number_of_users_deleted += 1
            except TSC.ServerResponseError as e:
                logger.error(" Server error occurred", e)
                number_of_errors += 1
                # TODO Map Error code
                # TODO implement --no-complete
            except ValueError:
                logger.error(" Could not delete user: User {} not found".format(username))
                number_of_errors += 1
        logger.info("======== 100% complete ========")
        logger.info("======== Number of users deleted from site: {} =========".format(number_of_users_deleted))
        if number_of_errors > 0:
            logger.info("======== Number of errors {} =========".format(number_of_errors))
