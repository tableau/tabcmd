import urllib

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
            logger.debug(req_option.get_query_params())
            matching_views, paging = server.views.get(req_option)
        except Exception as e:
            Errors.exit_with_error(logger, e)
        if len(matching_views) < 1:
            Errors.exit_with_error(logger, message=_("errors.xmlapi.not_found"))
        return matching_views[0]

    @staticmethod
    def get_wb_by_content_url(logger, server, workbook_content_url) -> TSC.WorkbookItem:
        logger.debug(_("export.status").format(workbook_content_url))
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter("contentUrl", TSC.RequestOptions.Operator.Equals, workbook_content_url))
            logger.debug(req_option.get_query_params())
            matching_workbooks, paging = server.workbooks.get(req_option)
        except Exception as e:
            Errors.exit_with_error(logger, e)
        if len(matching_workbooks) < 1:
            Errors.exit_with_error(logger, message=_("dataalerts.failure.error.workbookNotFound"))
        return matching_workbooks[0]

    @staticmethod
    def get_ds_by_content_url(logger, server, datasource_content_url) -> TSC.DatasourceItem:
        logger.debug(_("export.status").format(datasource_content_url))
        try:
            req_option = TSC.RequestOptions()
            req_option.filter.add(TSC.Filter("contentUrl", TSC.RequestOptions.Operator.Equals, datasource_content_url))
            logger.debug(req_option.get_query_params())
            matching_datasources, paging = server.datasources.get(req_option)
        except Exception as e:
            Errors.exit_with_error(logger, e)
        if len(matching_datasources) < 1:
            Errors.exit_with_error(logger, message=_("dataalerts.failure.error.datasourceNotFound"))
        return matching_datasources[0]

    @staticmethod
    def apply_values_from_url_params(logger, request_options: TSC.PDFRequestOptions, url) -> None:
        logger.debug(url)
        try:
            if "?" in url:
                query = url.split("?")[1]
                logger.debug("Query parameters: {}".format(query))
            else:
                logger.debug("No query parameters present in url")
                return

            params = query.split("&")
            logger.debug(params)
            for value in params:
                if value.startswith(":"):
                    DatasourcesAndWorkbooks.apply_options_in_url(logger, request_options, value)
                else:  # it must be a filter
                    DatasourcesAndWorkbooks.apply_encoded_filter_value(logger, request_options, value)

        except Exception as e:
            logger.warn("Error building filter params", e)
            # ExportCommand.log_stack(logger)  # type: ignore

    # this is called from within from_url_params, for each view_filter value
    @staticmethod
    def apply_encoded_filter_value(logger, request_options, value):
        # the REST API doesn't appear to have the option to disambiguate with "Parameters.<fieldname>"
        value = value.replace("Parameters.", "")
        # the filter values received from the url are already url encoded. tsc will encode them again.
        # so we run url.decode, which will be a no-op if they are not encoded.
        decoded_value = urllib.parse.unquote(value)
        logger.debug("url had `{0}`, saved as `{1}`".format(value, decoded_value))
        DatasourcesAndWorkbooks.apply_filter_value(logger, request_options, decoded_value)

    # this is called for each filter value,
    # from apply_options, which expects an un-encoded input,
    # or from apply_url_params via apply_encoded_filter_value which decodes the input
    @staticmethod
    def apply_filter_value(logger, request_options: TSC.PDFRequestOptions, value: str) -> None:
        logger.debug("handling filter param {}".format(value))
        if "=" not in value:
            Errors.exit_with_error(logger, message="Filter parameters must all be of the format parameter=value. "
                                   "Names and values cannot contain '=' or '&': encode these characters.")
        data_filter = value.split("=")
        if len(data_filter) != 2:
            Errors.exit_with_error(logger, message="Filter parameters must all be of the format parameter=value. "
                                   "Names and values cannot contain '=' or '&': encode these characters.")

        request_options.vf(data_filter[0], data_filter[1])

    # this is called from within from_url_params, for each param value
    @staticmethod
    def apply_options_in_url(logger, request_options: TSC.PDFRequestOptions, value: str) -> None:
        logger.debug("handling url option {}".format(value))
        setting = value.split("=")
        if len(setting) < 2:
            Errors.exit_with_error(logger, message="Filter parameters must all be of the format parameter=value. "
                                   "Names and values cannot contain '=' or '&': encode these characters.")
        if ":iid" == setting[0]:
            logger.debug(":iid value ignored in url")
        elif ":refresh" == setting[0] and DatasourcesAndWorkbooks.is_truthy(setting[1]):
            # mypy is worried that this is readonly
            request_options.max_age = 0  # type:ignore
            logger.debug("Set max age to {} from {}".format(request_options.max_age, value))
        elif ":size" == setting[0]:
            height, width = setting[1].split(",")
            logger.warn("Height/width parameters not yet implemented ({})".format(value))
        else:
            logger.debug("Parameter[s] not recognized: {}".format(value))

    @staticmethod
    def is_truthy(value: str):
        return value.lower() in ["yes", "y", "1", "true"]

    @staticmethod
    def apply_png_options(logger, request_options: TSC.ImageRequestOptions, args):
        if args.height or args.width:
            logger.warn("Height/width arguments not yet implemented in export")
        # Always request high-res images
        request_options.image_resolution = "high"

    @staticmethod
    def apply_pdf_options(logger, request_options: TSC.PDFRequestOptions, args):
        if args.pagelayout:
            request_options.orientation = args.pagelayout
        if args.pagesize:
            request_options.page_type = args.pagesize

    @staticmethod
    def save_to_data_file(logger, output, filename):
        logger.info(_("httputils.found_attachment").format(filename))
        with open(filename, "wb") as f:
            f.writelines(output)
            logger.info(_("export.success").format("", filename))

    @staticmethod
    def save_to_file(logger, output, filename):
        logger.info(_("Saving as {}").format(filename))
        with open(filename, "wb") as f:
            f.write(output)
            logger.info(_("export.success").format("", filename))
