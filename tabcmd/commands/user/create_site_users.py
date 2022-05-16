import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Constants
from tabcmd.execution.logger_config import log
from tabcmd.execution.global_options import *
from .user_data import UserCommand
from tabcmd.execution.localize import _


class CreateSiteUsersCommand(UserCommand):
    """
    Command to add users to a site, based on information supplied in a comma-separated values (CSV) file.
    If the user is not already created on the server, the command creates the user before adding
    that user to the site
    """

    name: str = "createsiteusers"
    description: str = "tabcmd.command.description.createsiteusers"

    @staticmethod
    def define_args(create_site_users_parser):
        set_role_arg(create_site_users_parser)
        set_users_file_positional(create_site_users_parser)
        set_completeness_options(create_site_users_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        number_of_users_listed = 0
        number_of_users_added = 0
        number_of_errors = 0

        creation_site = "current site"

        UserCommand.validate_file_for_import(args.filename, logger, detailed=True, strict=args.require_all_valid)

        logger.info(_("tabcmd.add.users.to_x").format(args.filename.name, creation_site))
        user_obj_list = UserCommand.get_users_from_file(args.filename, logger)
        logger.info(_("tabcmd.percentage.zero"))
        error_list = []
        for user_obj in user_obj_list:
            try:
                number_of_users_listed += 1
                result = server.users.add(user_obj)
                logger.info(_("tabcmd.result.success.create_user").format(user_obj.name))
                number_of_users_added += 1
            except TSC.ServerResponseError as e:
                number_of_errors += 1
                error_list.append(e)
                logger.debug(e)
        logger.info(_("tabcmd.percentage.hundred"))
        logger.info(_("importcsvsummary.line.processed").format(number_of_users_listed))
        logger.info(_("importcsvsummary.line.skipped").format(number_of_errors))
        logger.info(_("importcsvsummary.users.added.count").format(number_of_users_added))
        if number_of_errors > 0:
            logger.info(_("importcsvsummary.error.details").format(error_list))
