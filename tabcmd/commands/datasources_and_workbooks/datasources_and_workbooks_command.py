import tableauserverclient as TSC

from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.localize import _


class DatasourcesAndWorkbooks(Server):
    """
    Base Class for Operations related to Datasources and Workbooks
    """

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def get_view_url_from_names(wb_name, view_name):
        return "{}/sheets/{}".format(wb_name, view_name)

    @staticmethod
    def get_view_by_content_url(logger, server, view_content_url) -> TSC.ViewItem:
        logger.debug(_("export.status").format(view_content_url))
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter("contentUrl", TSC.RequestOptions.Operator.Equals, view_content_url))
            matching_views, paging = server.views.get(req_option)
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response").format(""))
        if len(matching_views) < 1:
            Errors.exit_with_error(logger, message=_("errors.xmlapi.not_found"))
        return matching_views[0]

    @staticmethod
    def get_wb_by_content_url(logger, server, workbook_content_url) -> TSC.WorkbookItem:
        logger.debug(_("export.status").format(workbook_content_url))
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter("contentUrl", TSC.RequestOptions.Operator.Equals, workbook_content_url))
            matching_workbooks, paging = server.workbooks.get(req_option)
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response").format(""))
        if len(matching_workbooks) < 1:
            Errors.exit_with_error(logger, message=_("dataalerts.failure.error.workbookNotFound"))
        return matching_workbooks[0]
        
    @staticmethod
    def get_ds_by_content_url(logger, server, datasource_content_url) -> TSC.DatasourceItem:
        logger.debug(_("export.status").format(datasource_content_url))
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter("contentUrl", TSC.RequestOptions.Operator.Equals, datasource_content_url))
            matching_datasources, paging = server.datasources.get(req_option)
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response").format(""))
        if len(matching_datasources) < 1:
            Errors.exit_with_error(logger, message=_("dataalerts.failure.error.datasourceNotFound"))
        return matching_datasources[0]
