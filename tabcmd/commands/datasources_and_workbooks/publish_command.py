import tableauserverclient as TSC

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
        set_parent_project_arg(group)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)

        if args.project_name:
            try:
                dest_project = Server.get_project_by_name_and_parent_path(
                    logger, server, args.project_name, args.parent_project_path
                )
                project_id = dest_project.id
            except Exception as exc:
                logger.error(exc.__str__())
                Errors.exit_with_error(logger, _("publish.errors.server_resource_not_found"), exc)
        else:
            project_id = ""
            args.project_name = "default"
            args.parent_project_path = ""

        publish_mode = PublishCommand.get_publish_mode(args)  # --overwrite, --replace
        logger.info("Publishing as " + publish_mode)

        if args.db_username:
            creds = TSC.models.ConnectionCredentials(args.db_username, args.db_password, embed=args.save_db_password)
        elif args.oauth_username:
            creds = TSC.models.ConnectionCredentials(args.oauth_username, None, embed=False, oauth=args.save_oauth)
        else:
            logger.debug("No db-username or oauth-username found in command")
            creds = None

        source = PublishCommand.get_filename_extension_if_tableau_type(logger, args.filename)
        logger.info(_("publish.status").format(args.filename))
        if source in ["twbx", "twb"]:
            new_workbook = TSC.WorkbookItem(project_id, name=args.name, show_tabs=args.tabbed)
            try:
                new_workbook = server.workbooks.publish(
                    new_workbook,
                    args.filename,
                    publish_mode,
                    connection_credentials=creds,
                    as_job=False,
                    skip_connection_check=False,
                )

            except IOError as ioe:
                Errors.exit_with_error(logger, ioe)
            logger.info(_("publish.success") + "\n{}".format(new_workbook.webpage_url))

        elif source in ["tds", "tdsx", "hyper"]:
            new_datasource = TSC.DatasourceItem(project_id, name=args.name)
            new_datasource.use_remote_query_agent = args.use_tableau_bridge
            try:
                new_datasource = server.datasources.publish(
                    new_datasource, args.filename, publish_mode, connection_credentials=creds
                )
            except IOError as ioe:
                Errors.exit_with_error(logger, exc)
            logger.info(_("publish.success") + "\n{}".format(new_datasource.webpage_url))

    @staticmethod
    def get_publish_mode(args):
        if args.overwrite:
            publish_mode = TSC.Server.PublishMode.Overwrite
        else:
            publish_mode = TSC.Server.PublishMode.CreateNew
        return publish_mode
