import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks
from tabcmd.execution.global_options import *
from tabcmd.commands.constants import Errors


class DeleteCommand(DatasourcesAndWorkbooks):
    """
    Command to delete the specified workbook or data source from the server.
    """

    name: str = "delete"
    description: str = "Delete a workbook or data source from the server"

    located_workbook = None
    located_datasource = None

    @staticmethod
    def define_args(delete_parser):
        set_ds_xor_wb_args(delete_parser)
        set_project_r_arg(delete_parser)
        set_parent_project_arg(delete_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)

        logger.info("===== Removing '{0}' from the server...".format(args.name or args.datasource or args.workbook))

        if args.workbook:
            item_type = "workbook"
            item_to_delete = DeleteCommand.get_workbook_item(logger, server, args.workbook)
        elif args.datasource:
            item_type = "datasource"
            item_to_delete = DeleteCommand.get_data_source_item(logger, server, args.datasource)
        else:
            try:
                item_to_delete = DeleteCommand.get_workbook_item(logger, server, args.name)
                item_type = "workbook"
            except TSC.ServerResponseError:
                try:
                    item_to_delete = DeleteCommand.get_data_source_item(logger, server, args.name)
                    item_type = "datasource"
                except TSC.ServerResponseError:
                    Errors.exit_with_error(logger, "You must specify a workbook or datasource")

        try:
            if item_type == "workbook":
                server.workbooks.delete(item_to_delete.id)
            else:
                server.datasources.delete(item_to_delete.id)
            logger.info("===== Succeeded")
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Error deleting from server", e)
