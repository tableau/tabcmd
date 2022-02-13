from ..commands import Commands
import tableauserverclient as TSC


class DatasourcesAndWorkbooks(Commands):
    """
    Base Class for Operations related to Datasources and Workbooks
    """
    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def get_request_option_for_view(logger, server, view_content_url):
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter(
                "contentUrl", TSC.RequestOptions.Operator.Equals, view_content_url))
            matching_views, _ = server.views.get(req_option)
            selected_view = matching_views[0]
            return selected_view
        except IndexError:
            Commands.exit_with_error(logger, "Could not find view. Please check the name and try again.")



    @staticmethod
    def get_request_option_for_workbook(logger, server, workbook_content_url):
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter(
                "contentUrl", TSC.RequestOptions.Operator.Equals, workbook_content_url))
            matching_workbooks, _ = server.workbooks.get(req_option)
            selected_workbook = matching_workbooks[0]
            return selected_workbook
        except IndexError:
            Commands.exit_with_error(logger, "Could not find view. Please check the name and try again.")
