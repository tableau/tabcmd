import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.site.site_command import SiteCommand
from tabcmd.commands.user.user_command import UserCommand
from tabcmd.execution.logger_config import log


class DeleteSiteUsersCommand(SiteCommand):
    """
    Command to Remove users from the site that user is logged in to.
    The users to be removed are specified in a file that contains
    a simple list of one user name per line.
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)

        number_of_users_deleted = 0
        number_of_errors = 0

        if args.require_all_valid:
            UserCommand.validate_file_for_import(args.users, logger)

        user_obj_list = UserCommand.get_users_from_file(args.filename)

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
            except ValueError:
                logger.error(" Could not delete user: User {} not found".format(username))
                number_of_errors += 1
        logger.info("======== 100% complete ========")
        logger.info("======== Number of users deleted from site: {} =========".format(number_of_users_deleted))
        logger.info("======== Number of errors {} =========".format(number_of_errors))
