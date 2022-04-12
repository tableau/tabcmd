import tableauserverclient as TSC

from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.commands.user.user_data import UserCommand
from tabcmd.execution.logger_config import log


class DeleteSiteUsersCommand(Server):
    """
    Command to Remove users from the site that user is logged in to.
    The users to be removed are specified in a file that contains
    a simple list of one user name per line.
    """

    name: str = "deletesiteusers"
    description: str = "Delete site users"

    @staticmethod
    def define_args(delete_site_users_parser):
        set_users_file_positional(delete_site_users_parser)
        set_completeness_options(delete_site_users_parser)

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)

        if args.site_name:
            target_site = args.site_name
        else:
            target_site = "current site"

        logger.info("Deleting users listed in {0} from site '{1}'".format(args.filename.name, target_site))

        UserCommand.validate_file_for_import(args.filename, logger, strict=args.require_all_valid)
        number_of_users_deleted = 0
        number_of_errors = 0
        user_obj_list = UserCommand.get_users_from_file(args.filename, logger)

        logger.debug("Successfully parsed {} users".format(len(user_obj_list)))
        logger.info("======== 0% complete ========")

        error_list = []
        for user_obj in user_obj_list:
            user_id = UserCommand.find_user_id(logger, server, user_obj.name)
            try:
                server.users.remove(user_id)
                logger.info("Successfully deleted user from site: {}".format(user_obj.name))
                number_of_users_deleted += 1
            except TSC.ServerResponseError as e:
                Errors.check_common_error_codes_and_explain(logger.info, e)
                number_of_errors += 1
                error_list.append(e)
            except ValueError:
                logger.error(" Could not delete user: User {} not found".format(user_obj.name))
                error_list.append(e)
                number_of_errors += 1
        logger.info("======== 100% complete ========")
        logger.info("======== Number of users deleted from site: {} =========".format(number_of_users_deleted))
        logger.info("======== Number of errors {} =========".format(number_of_errors))
        if number_of_errors > 0:
            logger.info("Error details: \n{}".format(error_list))
