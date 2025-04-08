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
            Errors.exit_with_error(logger, exception=e)
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
            Errors.exit_with_error(logger, exception=e)
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
            Errors.exit_with_error(logger, exception=e)
        if len(matching_datasources) < 1:
            Errors.exit_with_error(logger, message=_("errors.publish.datasource.not.found"))
        return matching_datasources[0]

    @staticmethod
    def apply_values_from_url_params(logger, request_options: TSC.RequestOptions, url) -> None:
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
    def apply_filter_value(logger, request_options: TSC.RequestOptions, value: str) -> None:
        logger.debug("handling filter param {}".format(value))
        data_filter = value.split("=")
        # we should export the _DataExportOptions class from tsc
        request_options.vf(data_filter[0], data_filter[1])  # type: ignore

    # this is called from within from_url_params, for each param value
    # expects either ImageRequestOptions or PDFRequestOptions
    @staticmethod
    def apply_options_in_url(logger, request_options: TSC.RequestOptions, value: str) -> None:
        logger.debug("handling url option {}".format(value))
        setting = value.split("=")
        if len(setting) != 2:
            logger.warn("Unable to read url parameter '{}', skipping".format(value))
            return
        setting_name = setting[0]
        setting_val = setting[1]
        logger.debug("setting named {}, has value {}".format(setting_name, setting_val))

        if ":iid" == setting_name:
            logger.debug(":iid value ignored in url")
        elif ":refresh" == setting_name and DatasourcesAndWorkbooks.is_truthy(setting_val):
            # mypy is worried that this is readonly
            request_options.max_age = 0  # type: ignore
            logger.debug("Set max age to {} from {}".format((TSC.ImageRequestOptions(request_options)).max_age, value))
        elif ":size" == setting_name:
            if isinstance(request_options, (TSC.ImageRequestOptions, TSC.PDFRequestOptions)):
                try:
                    height, width = setting_val.split(",")
                    request_options.viz_height = int(height)
                    request_options.viz_width = int(width)
                except Exception as oops:
                    logger.warn("Unable to read image size options '{}', skipping".format(setting_val))
                    logger.warn(oops)
            else:
                logger.debug(
                    "Request options are not of type ImageRequestOptions or PDFRequestOptions, skipping size setting"
                )
        else:
            logger.debug("Parameter[s] not recognized: {}".format(value))

    @staticmethod
    def is_truthy(value: str):
        return value.lower() in ["yes", "y", "1", "true"]

    @staticmethod
    def apply_png_options(logger, request_options: TSC.ImageRequestOptions, args):
        # these are only used in export, not get
        if args.height:
            request_options.viz_height = int(args.height)
        if args.width:
            request_options.viz_width = int(args.width)
        if args.resolution and args.resolution != TSC.ImageRequestOptions.Resolution.High.lower():
            request_options.image_resolution = None
        else:
            request_options.image_resolution = TSC.ImageRequestOptions.Resolution.High.lower()
        if args.language:
            request_options.language = args.language

    @staticmethod
    def apply_pdf_options(logger, request_options: TSC.PDFRequestOptions, args):
        if args.pagelayout:
            request_options.orientation = args.pagelayout
        if args.pagesize:
            request_options.page_type = args.pagesize
        if args.language:
            request_options.language = args.language

    @staticmethod
    def apply_csv_options(logger, request_options: TSC.CSVRequestOptions, args):
        if args.language:
            request_options.language = args.language

    @staticmethod
    def save_to_data_file(logger, output, filename):
        logger.info(_("httputils.found_attachment").format(filename))
        with open(filename, "wb") as f:
            f.writelines(output)
            logger.info(_("export.success").format("", filename))

    @staticmethod
    def save_to_file(logger, output, filename):
        logger.info(_("httputils.found_attachment").format(filename))
        with open(filename, "wb") as f:
            f.write(output)
            logger.info(_("export.success").format("", filename))

    @staticmethod
    def get_custom_view_by_id(logger, server, custom_view_id) -> TSC.CustomViewItem:
        logger.debug(_("export.status").format(custom_view_id))
        try:
            matching_custom_view = server.custom_views.get_by_id(custom_view_id)
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)
        if matching_custom_view is None:
            Errors.exit_with_error(logger, message=_("errors.xmlapi.not_found"))
        return matching_custom_view
