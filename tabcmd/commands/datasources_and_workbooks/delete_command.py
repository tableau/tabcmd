import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks
from tabcmd.execution.global_options import *
from tabcmd import _


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
        delete_parser_group = delete_parser.add_mutually_exclusive_group(required=True)
        delete_parser_group.add_argument("name", nargs="?", help="The datasource or workbook to delete")
        delete_parser_group.add_argument("--workbook", required=False, help=_("delete.options.workbook"))
        delete_parser_group.add_argument("--datasource", required=False, help=_("delete.options.datasource"))
        set_project_r_arg(delete_parser)
        set_parent_project_arg(delete_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)

        logger.info(_("delete.status").format(args.name or args.datasource or args.workbook))

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
                    DeleteCommand.exit_with_error(logger, "You must specify a workbook or datasource")

        try:
            if item_type == "workbook":
                server.workbooks.delete(item_to_delete.id)
            else:
                server.datasources.delete(item_to_delete.id)
            logger.info("===== Succeeded")
        except TSC.ServerResponseError as e:
            DeleteCommand.exit_with_error(logger, "Error deleting from server", e)
