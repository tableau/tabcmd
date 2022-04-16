import tableauserverclient as TSC
from tabcmd.commands.server import Server
from tabcmd.commands.constants import Errors


class DatasourcesAndWorkbooks(Server):
    """
    Base Class for Operations related to Datasources and Workbooks
    """

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def get_view_by_content_url(logger, server, view_content_url) -> TSC.ViewItem:
        logger.debug("Fetching view with id {}".format(view_content_url))
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter("contentUrl", TSC.RequestOptions.Operator.Equals, view_content_url))
            matching_views, _ = server.views.get(req_option)
            selected_view = matching_views[0]
            return selected_view
        except Exception as e:
            Errors.exit_with_error(logger, "Could not find view. Please check the name and try again.", e)

    @staticmethod
    def get_wb_by_content_url(logger, server, workbook_content_url) -> TSC.WorkbookItem:
        logger.debug("fetch workbook with id {}".format(workbook_content_url))
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(
                TSC.Filter(
                    "contentUrl",
                    TSC.RequestOptions.Operator.Equals,
                    workbook_content_url,
                )
            )
            matching_workbooks, _ = server.workbooks.get(req_option)
            selected_workbook = matching_workbooks[0]
            return selected_workbook
        except Exception:
            Errors.exit_with_error(logger, "Could not find workbook. Please check the name and try again.")
