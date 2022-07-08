import tableauserverclient as TSC

from src.commands.auth.session import Session
from src.commands.constants import Errors
from src.commands.server import Server
from src.execution.global_options import *
from src.execution.localize import _
from src.execution.logger_config import log
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
        publish_parser.add_argument(
            "filename",
            metavar="filename.twbx|tdsx|hyper",
            # this is not actually a File type because we just pass the path to tsc
        )
        set_publish_args(publish_parser)
        set_project_r_arg(publish_parser)
        set_parent_project_arg(publish_parser)

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
                Errors.exit_with_error(
                    logger, _("publish.errors.server_resource_not_found"), exc
                )
        else:
            project_id = ""
            args.project_name = "default"
            args.parent_project_path = ""

        publish_mode = PublishCommand.get_publish_mode(args)
        logger.info("Publishing as " + publish_mode)

        source = PublishCommand.get_filename_extension_if_tableau_type(
            logger, args.filename
        )
        logger.info(_("publish.status").format(args.filename))
        if source in ["twbx", "twb"]:
            new_workbook = TSC.WorkbookItem(
                project_id, name=args.name, show_tabs=args.tabbed
            )
            try:
                new_workbook = server.workbooks.publish(
                    new_workbook, args.filename, publish_mode
                )
            except IOError as ioe:
                Errors.exit_with_error(logger, ioe)
            logger.info(_("publish.success") + "\n{}".format(new_workbook.webpage_url))

        elif source in ["tds", "tdsx", "hyper"]:
            new_datasource = TSC.DatasourceItem(project_id, name=args.name)
            try:
                new_datasource = server.datasources.publish(
                    new_datasource, args.filename, publish_mode
                )
            except IOError as ioe:
                Errors.exit_with_error(logger, exc)
            logger.info(
                _("publish.success") + "\n{}".format(new_datasource.webpage_url)
            )

    @staticmethod
    def get_publish_mode(args):
        if args.overwrite:
            publish_mode = TSC.Server.PublishMode.Overwrite
        else:
            publish_mode = TSC.Server.PublishMode.CreateNew
        return publish_mode
