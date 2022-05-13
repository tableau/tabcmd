import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.execution.logger_config import log
from tabcmd.execution.global_options import *
from .user_data import UserCommand
from tabcmd.execution.localize import _


class CreateUsersCommand(UserCommand):
    """
    Command to add users to a site, based on information supplied in a comma-separated values (CSV) file.
    If the user is not already created on the server, the command creates the user before adding
    that user to the site
    """

    name: str = "createUsers"
    description: str = "tabcmd.command.description.create_users"

    @staticmethod
    def define_args(create_users_parser):
        set_role_arg(create_users_parser)
        set_users_file_positional(create_users_parser)
        set_completeness_options(create_users_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
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

        logger.info(_("tabcmd.add.users.to_x").format(args.filename.name, creation_site))
        user_obj_list = UserCommand.get_users_from_file(args.filename, logger)
        logger.info("tabcmd.percentage.zero")
        error_list = []
        for user_obj in user_obj_list:
            try:
                number_of_users_listed += 1
                # TODO: bring in other attributes in file, actually act on specific site
                new_user = TSC.UserItem(user_obj.name, args.role)
                server.users.add(new_user)
                logger.info("tabcmd.result.success.create_user".format(user_obj.name))
                number_of_users_added += 1
            except Exception as e:
                number_of_errors += 1
                error = "tabcmd.result.failed.create.user".format(e)
                error_list.append(error)
                logger.debug(error)
        logger.info("tabcmd.percentage.hundred")
        logger.info("tabcmd.report.lines_processed".format(number_of_users_listed))
        logger.info("tabcmd.report.lines_skipped".format(number_of_errors))
        logger.info("tabcmd.report.users_added".format(number_of_users_added))
        if number_of_errors > 0:
            logger.debug("tabcmd.report.errors".format(number_of_errors))
        for exception in error_list:
            Errors.check_common_error_codes_and_explain(logger, exception)
