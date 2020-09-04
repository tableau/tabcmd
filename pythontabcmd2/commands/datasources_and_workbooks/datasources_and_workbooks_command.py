from ..commands import Commands
import tableauserverclient as TSC


class DatasourcesAndWorkbooks(Commands):
    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def get_request_option_for_view(self, server, view):
        req_option = TSC.RequestOptions()
        req_option.filter.add(TSC.Filter("contentUrl",
                                         TSC.RequestOptions.
                                         Operator.Equals,
                                         view))
        matching_view, _ = server.views.get(
            req_option)
        views_from_list = matching_view[0]
        return views_from_list

    def get_request_option_for_workbook(self, server, workbook):
        req_option = TSC.RequestOptions()
        req_option.filter.add(TSC.Filter("contentUrl",
                                         TSC.RequestOptions.
                                         Operator.Equals,
                                         workbook))
        matching_workbook, _ = server.workbooks.get(
            req_option)
        workbook_from_list = matching_workbook[0]
        return workbook_from_list
