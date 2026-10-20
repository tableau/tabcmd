import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .user_data import UserCommand


class CreateUsersCommand(UserCommand):
    """
    Command to add users to a site, based on information supplied in a comma-separated values (CSV) file.
    If the user is not already created on the server, the command creates the user before adding
    that user to the site
    """

    name: str = "createUsers"
    description: str = _("createusers.short_description")

    @staticmethod
    def define_args(create_users_parser):
        args_group = create_users_parser.add_argument_group(title=CreateUsersCommand.name)
        UserCommand.set_role_arg(args_group)
        set_users_file_positional(args_group)
        set_completeness_options(args_group)
        UserCommand.set_auth_arg(args_group)

    @classmethod
    def run_command(cls, args):
        logger = log(cls.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)
        number_of_users_listed = 0
        number_of_users_added = 0
        number_of_errors = 0

        ## TODO
        # If the server has only one site (the default site), the user is created and added to the site.
        # If the server has multiple sites, the user is created but is not added to any site.
        # To add users to a site, use createsiteusers.
        if args.site_name:
            creation_site = args.site_name
        else:
            creation_site = "current site"

        UserCommand.validate_file_for_import(args.filename, logger, detailed=True, strict=args.require_all_valid)

        logger.info(_("createusers.status").format(args.filename.name))
        # A --auth-type override replaces any CSV-supplied auth value, so suppress
        # the CSV-time "Local" remap warning when one is given -- it would describe
        # a value that's about to be discarded.
        user_obj_list = UserCommand.get_users_from_file(
            args.filename, logger, warn_on_local_remap=not getattr(args, "auth_type", None)
        )
        logger.info(_("session.monitorjob.percent_complete").format(0))
        error_list = []
        for user_obj in user_obj_list:
            try:
                number_of_users_listed += 1
                if args.role:
                    user_obj.site_role = args.role
                if args.auth_type:
                    user_obj.auth_setting = UserCommand.normalize_auth_setting(args.auth_type, user_obj.name, logger)
                server.users.add(user_obj)
                logger.info(_("common.output.succeeded").format(user_obj.name))
                number_of_users_added += 1
            except Exception as e:
                if Errors.is_resource_conflict(e) and args.continue_if_exists:
                    logger.info(_("tabcmd.errors.user_already_exists").format(user_obj.name))
                    continue

                number_of_errors += 1
                error_list.append(e)
                logger.debug(e)
        logger.info(_("session.monitorjob.percent_complete").format(100))
        logger.info(_("importcsvsummary.line.processed").format(number_of_users_listed))
        logger.info(_("importcsvsummary.line.skipped").format(number_of_errors))
        logger.info(_("importcsvsummary.users.added.count").format(number_of_users_added))
        if number_of_errors > 0:
            logger.info(_("importcsvsummary.error.details"))
        for exception in error_list:
            Errors.check_common_error_codes_and_explain(logger, exception)
