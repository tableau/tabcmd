import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Constants
from tabcmd.execution.logger_config import log
from tabcmd.execution.global_options import *
from .user_data import UserCommand


class CreateUsersCommand(UserCommand):
    """
    Command to add users to a site, based on information supplied in a comma-separated values (CSV) file.
    If the user is not already created on the server, the command creates the user before adding
    that user to the site
    """

    name: str = "createUsers"
    description: str = "Create users on the current site"

    @staticmethod
    def define_args(create_users_parser):
        set_role_arg(create_users_parser)
        set_users_file_positional(create_users_parser)
        set_completeness_options(create_users_parser)

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        number_of_users_listed = 0
        number_of_users_added = 0
        number_of_errors = 0

        if args.site_name:
            creation_site = args.site_name
        else:
            creation_site = "current site"

        UserCommand.validate_file_for_import(args.filename, logger, detailed=True, strict=args.require_all_valid)

        logger.info("===== Adding users listed in {0} to {1}...".format(args.filename.name, creation_site))
        user_obj_list = UserCommand.get_users_from_file(args.filename, logger)
        logger.info("======== 0% complete ========")
        error_list = []
        for user_obj in user_obj_list:
            try:
                number_of_users_listed += 1
                # TODO: bring in other attributes in file, actually act on specific site
                new_user = TSC.UserItem(user_obj.name, args.role)
                result = server.users.add(new_user)
                print(result)
                logger.info("Successfully created user: {}".format(user_obj.name))
                number_of_users_added += 1
            except TSC.ServerResponseError as e:
                number_of_errors += 1
                logger.debug("Failed to add user: {}".format(e))
                if e.code == Constants.forbidden:
                    error = "User is not local, and the user's credentials are not maintained on Tableau Server."
                if e.code == Constants.invalid_credentials:
                    error = "Unauthorized access, Please log in."
                if e.code == Constants.user_already_member_of_site:
                    error = "User: {} already member of site".format(user_obj.name)
                error_list.append(error)
                logger.debug(error)
        logger.info("======== 100% complete ========")
        logger.info("======== Lines processed: {} =========".format(number_of_users_listed))
        logger.info("Lines skipped: {}".format(number_of_errors))
        logger.info("Number of users added: {}".format(number_of_users_added))
        if number_of_errors > 0:
            logger.info("Error details: {}".format(error_list))
