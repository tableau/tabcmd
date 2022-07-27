import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class DeleteCommand(DatasourcesAndWorkbooks):
    """
    Command to delete the specified workbook or data source from the server.
    """

    name: str = "delete"
    description: str = _("delete.short_description")

    located_workbook = None
    located_datasource = None

    @staticmethod
    def define_args(delete_parser):
        delete_parser.add_argument("name", help=_("content_type.workbook") + "/" + _("content_type.datasource"))
        set_ds_xor_wb_options(delete_parser)
        set_project_r_arg(delete_parser)
        set_parent_project_arg(delete_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        content_type: str = ""
        if args.workbook:
            content_type = "workbook"
        elif args.datasource:
            content_type = "datasource"

        container: TSC.ProjectItem = DeleteCommand.get_project_by_name_and_parent_path(
            logger, server, args.project_name, args.parent_project_path
        )
        if container:
            item_name = (args.parent_project_path or "") + "/" + (args.project_name or "default") + "/" + args.name
        else:
            Errors.exit_with_error(logger, "Containing project could not be found")
        logger.info(_("delete.status").format(content_type, item_name or args.name))

        error = None
        if args.workbook or not content_type:
            logger.debug("Attempt as workbook")
            try:
                item_to_delete = DeleteCommand.get_workbook_item(logger, server, args.name, container)
                content_type = "workbook"
            except TSC.ServerResponseError as error:
                logger.debug(error)
        if args.datasource or not content_type:
            logger.debug("Attempt as datasource")
            try:
                item_to_delete = DeleteCommand.get_data_source_item(logger, server, args.name, container)
                content_type = "datasource"
            except TSC.ServerResponseError as error:
                logger.debug(error)
        if not content_type or not item_to_delete:
            logger.debug(error)
            Errors.exit_with_error(logger, _("delete.errors.requires_workbook_datasource"))

        try:
            if content_type == "workbook":
                server.workbooks.delete(item_to_delete.id)
            else:
                server.datasources.delete(item_to_delete.id)
            logger.info(_("common.output.succeeded"))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Error deleting from server", e)
