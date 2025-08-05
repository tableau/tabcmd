import tableauserverclient as TSC
from tableauserverclient import ServerResponseError

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class PublishCommand(DatasourcesAndWorkbooks):
    """
    This command publishes the specified workbook (.twb(x)), data source
    (.tds(x)), or extract (.hyper) to Tableau Server.
    """

    name: str = "publish"
    description: str = _("publish.description")

    @staticmethod
    def define_args(publish_parser):
        group = publish_parser.add_argument_group(title=PublishCommand.name)
        group.add_argument(
            "filename",
            metavar="filename.twbx|tdsx|hyper",
            # this is not actually a File type because we just pass the path to tsc
        )
        set_publish_args(group)
        set_project_r_arg(group)
        set_overwrite_option(group)
        set_append_replace_option(group)
        set_parent_project_arg(group)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)

        if not args.project_name:
            args.project_name = "Default"
            args.parent_project_path = ""
        try:
            dest_project = Server.get_project_by_name_and_parent_path(
                logger, server, args.project_name, args.parent_project_path
            )
            project_id = dest_project.id
        except Exception as exc:
            logger.error(exc.__str__())
            Errors.exit_with_error(logger, _("publish.errors.server_resource_not_found"), exc)

        publish_mode = PublishCommand.get_publish_mode(args, logger)

        connection = TSC.models.ConnectionItem()
        if args.db_username:
            connection.connection_credentials = TSC.models.ConnectionCredentials(
                args.db_username, args.db_password, embed=args.save_db_password
            )
        elif args.oauth_username:
            connection.connection_credentials = TSC.models.ConnectionCredentials(
                args.oauth_username, None, embed=False, oauth=args.save_oauth
            )
        else:
            logger.debug("No db-username or oauth-username found in command")
            connection = None

        if connection:
            connections = list()
            connections.append(connection)
        else:
            connections = None

        source = PublishCommand.get_filename_extension_if_tableau_type(logger, args.filename)
        logger.info(_("publish.status").format(args.filename))
        if source in ["twbx", "twb"]:
            if args.thumbnail_username and args.thumbnail_group:
                raise AttributeError("Cannot specify both a user and group for thumbnails.")

            new_workbook = TSC.WorkbookItem(project_id, name=args.name, show_tabs=args.tabbed)
            if args.thumbnail_username:
                new_workbook.thumbnails_user_id = args.thumbnail_username
            elif args.thumbnail_group:
                new_workbook.thumbnails_group_id = args.thumbnail_group

            try:
                new_workbook = server.workbooks.publish(
                    new_workbook,
                    args.filename,
                    publish_mode,
                    connections=connections,
                    as_job=False,
                    skip_connection_check=args.skip_connection_check,
                )
            except Exception as e:
                Errors.exit_with_error(logger, exception=e)

            logger.info(_("publish.success") + "\n{}".format(new_workbook.webpage_url))

        elif source in ["tds", "tdsx", "hyper"]:
            new_datasource = TSC.DatasourceItem(project_id, name=args.name)
            new_datasource.use_remote_query_agent = args.use_tableau_bridge
            try:
                new_datasource = server.datasources.publish(
                    new_datasource, args.filename, publish_mode, connections=connections
                )
            except Exception as exc:
                Errors.exit_with_error(logger, exception=exc)
            logger.info(_("publish.success") + "\n{}".format(new_datasource.webpage_url))

    # todo write tests for this method
    @staticmethod
    def get_publish_mode(args, logger):
        # default: fail if it already exists on the server
        default_mode = TSC.Server.PublishMode.CreateNew
        publish_mode = default_mode

        mode_mapping = {
            "replace": TSC.Server.PublishMode.Replace,
            "append": TSC.Server.PublishMode.Append,
            "overwrite": TSC.Server.PublishMode.Overwrite,
        }

        selected_modes = [mode for mode, mode_value in mode_mapping.items() if getattr(args, mode, False)]

        if len(selected_modes) > 1:
            Errors.exit_with_error(logger, "Invalid combination of publishing options (Append, Overwrite, Replace)")

        if selected_modes:
            publish_mode = mode_mapping[selected_modes[0]]

        logger.debug("Publish mode selected: " + publish_mode)
        return publish_mode
