import tableauserverclient as TSC
import glob
import os

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
            # this is a string and not actually a File type because we just pass the path to tsc
            metavar="filename.twbx|tdsx|hyper",
            help="The specified file to publish. If a folder is given, it will publish all files in this folder \
                that have the extensions twb, twbx, tdsx or hyper. Any other options set will be applied for all files."
        )
        group.add_argument("--filetype", metavar="twb|twbx|tdxs|hyper", help="If publishing an entire folder, limit files to this filetype.")
        group.add_argument("--recursive", help="If publishing an entire folder, look into subdirectories to find files")
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

        if args.db_username:
            creds = TSC.models.ConnectionCredentials(args.db_username, args.db_password, embed=args.save_db_password)
        elif args.oauth_username:
            creds = TSC.models.ConnectionCredentials(args.oauth_username, None, embed=False, oauth=args.save_oauth)
        else:
            logger.debug("No db-username or oauth-username found in command")
            creds = None
        credentials = TSC.ConnectionItem() if creds else None
        if credentials:
            credentials.connection_credentials = creds

        files = PublishCommand.get_files_to_publish(args, logger)

        logger.debug("Publishing {} files".format(len(files)))
        for str_filename in files:
            source = PublishCommand.get_filename_extension_if_tableau_type(logger, str_filename)
            logger.info(_("publish.status").format(str_filename))
            if source in ["twbx", "twb"]:
                if args.thumbnail_group:
                    raise AttributeError("Generating thumbnails for a group is not yet implemented.")
                if args.thumbnail_username and args.thumbnail_group:
                    raise AttributeError("Cannot specify both a user and group for thumbnails.")

                new_workbook = TSC.WorkbookItem(project_id, name=args.name, show_tabs=args.tabbed)
                try:
                    new_workbook = server.workbooks.publish(
                        new_workbook,
                        str_filename,
                        publish_mode,
                        # args.thumbnail_username, not yet implemented in tsc
                        # args.thumbnail_group,
                        connections=credentials,
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
                        new_datasource, str_filename, publish_mode, connection_credentials=creds
                    )
                except Exception as exc:
                    Errors.exit_with_error(logger, exception=exc)
                logger.info(_("publish.success") + "\n{}".format(new_datasource.webpage_url))

    @staticmethod
    def get_files_to_publish(args, logger):
        logger.debug("Checking file argument: {}".format(args.filename))
        files = []
        if not os.path.exists(args.filename):
            logger.debug("Invalid file")
            Errors.exit_with_error(logger, message="Filename given does not exist: {}".format(args.filename))
        elif os.path.isfile(args.filename):
            logger.debug("Valid single file found")
            files.append(args.filename)
        elif os.path.isdir(args.filename):            
            logger.debug("Valid folder found")
            if args.filetype:
                file_patterns = [args.filetype]
            else:
                file_patterns = ['*.twb?', '*.tdsx', '*.hyper']
            logger.debug("file patterns: {}".format(file_patterns))
            for file_pattern in file_patterns:
                logger.debug("Looking for files {} in {}".format(file_pattern, args.filename))
                try:
                    in_place_files = (glob.glob(file_pattern, root_dir=args.filename, recursive=args.recursive, include_hidden=False))
                    relative_files = map(lambda file: os.path.join(args.filename, file), in_place_files)
                except Exception as e:            
                    Errors.exit_with_error(logger, e)
                files.extend(relative_files)
                logger.debug(len(files))
        return files

    # todo write tests for this method
    @staticmethod
    def get_publish_mode(args, logger):
        # default: fail if it already exists on the server
        default_mode = TSC.Server.PublishMode.CreateNew
        publish_mode = default_mode

        if args.replace:
            raise AttributeError("Replacing an extract is not yet implemented")

        if args.append:
            if publish_mode != default_mode:
                publish_mode = None
            else:
                # only relevant for datasources, but tsc will throw an error for us if necessary
                publish_mode = TSC.Server.PublishMode.Append

        if args.overwrite:
            if publish_mode != default_mode:
                publish_mode = None
            else:
                # Overwrites the workbook, data source, or data extract if it already exists on the server.
                publish_mode = TSC.Server.PublishMode.Overwrite

        if not publish_mode:
            Errors.exit_with_error(logger, "Invalid combination of publishing options (Append, Overwrite, Replace)")
        logger.debug("Publish mode selected: " + publish_mode)
        return publish_mode
