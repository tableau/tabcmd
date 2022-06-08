import tableauserverclient as TSC

from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.commands.user.user_data import UserCommand
from tabcmd.execution.logger_config import log
from tabcmd.execution.localize import _


class DeleteSiteUsersCommand(Server):
    """
    Command to Remove users from the site that user is logged in to.
    The users to be removed are specified in a file that contains
    a simple list of one user name per line.
    """

    name: str = "deletesiteusers"
    description: str = _("deletesiteusers.short_description")

    @staticmethod
    def define_args(delete_site_users_parser):
        set_users_file_positional(delete_site_users_parser)
        set_completeness_options(delete_site_users_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)

        logger.info(_("deleteusers.status").format(args.filename.name))

        UserCommand.validate_file_for_import(args.filename, logger, strict=args.require_all_valid)
        number_of_users_deleted = 0
        number_of_errors = 0
        user_obj_list = UserCommand.get_users_from_file(args.filename, logger)

        logger.debug("Users: {}".format(len(user_obj_list)))

        error_list = []
        for user_obj in user_obj_list:
            logger.info(_("importcsvsummary.line.processed").format(number_of_users_deleted))
            try:
                user_id = UserCommand.find_user_id(logger, server, user_obj.name)
                server.users.remove(user_id)
                logger.debug(_("tabcmd.result.success.delete_user").format(user_obj.name, user_id))
                number_of_users_deleted += 1
            except Exception as e:
                Errors.check_common_error_codes_and_explain(logger, e)
                number_of_errors += 1
                error_list.append(e)

        logger.info(_("importcsvsummary.line.processed").format(number_of_users_deleted))
        logger.info(_("importcsvsummary.errors.count").format(number_of_errors))
        if number_of_errors > 0:
            logger.info(_("importcsvsummary.error.details").format(error_list))
