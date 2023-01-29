from tabcmd.commands.constants import Errors
from tabcmd.commands.datasources_and_workbooks.datasources_and_workbooks_command import DatasourcesAndWorkbooks
from tabcmd.commands.server import Server
from tabcmd.execution.localize import _

import tableauserverclient as TSC


class Extracts(Server):

    @staticmethod
    def get_wb_or_ds_for_extracts(args, logger, server):
        container = Server.get_project_by_name_and_parent_path(logger, server, args.project, args.parent_path)
        if args.datasource:
            logger.debug(_("export.status").format(args.datasource))
            datasource = Server.get_data_source_item(
                logger, server, args.datasource, container)
            return datasource

        elif args.workbook or args.url:
            logger.debug(_("export.status").format(args.workbook))
            if args.url:
                workbook_item: TSC.WorkbookItem = \
                    DatasourcesAndWorkbooks.get_wb_by_content_url(logger, server, args.url)
            elif args.workbook:
                workbook_item = Server.get_workbook_item(
                    logger, server, args.workbook, container)
            return workbook_item

        Errors.exit_with_error(logger, "Datasource or workbook required")
