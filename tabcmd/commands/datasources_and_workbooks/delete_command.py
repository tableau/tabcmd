import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks
from tabcmd.execution.global_options import *
from tabcmd.commands.constants import Errors
from tabcmd.execution.localize import _


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
        delete_parser.add_argument("name", help=_("content_type.workbook") + _("content_type.datasource"))
        set_project_r_arg(delete_parser)
        set_parent_project_arg(delete_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)

        logger.info(_("delete.status").format(args.name, ""))


        error = None
        try:
            item_to_delete = DeleteCommand.get_workbook_item(logger, server, args.name)
            item_type = "workbook"
        except TSC.ServerResponseError as workbook_error:
            error = workbook_error
        try:
            item_to_delete = DeleteCommand.get_data_source_item(logger, server, args.name)
            item_type = "datasource"
        except TSC.ServerResponseError as ds_error:
            error = ds_error
        if not item_type:
            logger.debug(error)
            Errors.exit_with_error(logger, _("delete.errors.requires_workbook_datasource"))

        try:
            if item_type == "workbook":
                server.workbooks.delete(item_to_delete.id)
            else:
                server.datasources.delete(item_to_delete.id)
            logger.info(_("common.output.succeeded"))
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Error deleting from server", e)
