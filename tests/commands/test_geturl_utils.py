import unittest
from typing import Iterator
from unittest import mock

import tableauserverclient

from tabcmd.commands.datasources_and_workbooks.get_url_command import *
from tabcmd.commands.datasources_and_workbooks.export_command import *
from tabcmd.commands.server import Server

mock_args = argparse.Namespace()
mock_args.pagelayout = None
mock_args.pagesize = None
mock_args.image_resolution = None
mock_args.width = None
mock_args.height = None
mock_args.filename = None
mock_args.filter = None

mock_logger = mock.MagicMock()

fake_item = mock.MagicMock(TSC.ViewItem)
fake_item.name = "fake-name"
fake_item.id = "fake-id"


class FileHandling(unittest.TestCase):

    # get_file_type_from_filename(logger, url, filename)
    # get_file_extension(filepath)
    # evaluate_content_type(logger, url)
    # strip_query_params(filename)
    # get_name_without_possible_extension(fileanme)
    # get_resource_name(url, logger)
    # get_view_url(url, logger)
    # filename_from_args(file_arg, item_name, filetype)

    def test_get_view_with_chars_in_save_name(self):
        filename = "C:\\chase.culver\\docs\\downloaded.twbx"  # W-13757625 fails if file path contains .
        url = None
        filetype = GetUrl.get_file_type_from_filename(mock_logger, filename, url)
        assert filetype == "twbx", filetype

    def test_evaluate_file_name_pdf(self):
        filename = "filename.pdf"
        url = None
        filetype = GetUrl.get_file_type_from_filename(mock_logger, filename, url)
        assert filetype == "pdf", filetype

    def test_evaluate_file_name_url(self):
        filename = "filename.twbx"
        filetype = Server.get_filename_extension_if_tableau_type(mock_logger, filename)
        assert filetype == "twbx", filetype

    def test_evaluate_file_path(self):
        filename = "../assets/filename.twb"
        filetype = Server.get_filename_extension_if_tableau_type(mock_logger, filename)
        assert filetype == "twb", filetype

    def test_evaluate_file_name_url_pdf_fails(self):
        filename = "filename.pdf"
        with self.assertRaises(ValueError):
            filetype = Server.get_filename_extension_if_tableau_type(mock_logger, filename)

    def test_evaluate_file_name_url_no_ext_fails(self):
        filename = "filename/filename/filename/file"
        with self.assertRaises(ValueError):
            filetype = Server.get_filename_extension_if_tableau_type(mock_logger, filename)

    def test_get_view_without_extension_that_does_have_one(self):
        filename = "viewname.pdf"
        assert GetUrl.get_name_without_possible_extension(filename) == "viewname"

    def test_get_view_without_extension_that_doesnt_have_one(self):
        filename = "viewname"
        assert GetUrl.get_name_without_possible_extension(filename) == filename


# handling our specific url-ish identifiers: /workbook/wb-name, etc
class GeturlTests(unittest.TestCase):
    def test_get_workbook_name(self):
        assert GetUrl.get_resource_name("workbooks/wbname", mock_logger) == "wbname"

    def test_view_name(self):
        assert GetUrl.get_view_url("views/wb-name/view-name", None) == "wb-name/sheets/view-name"

    def test_view_name_with_url_params(self):
        assert GetUrl.get_view_url("views/wb-name/view-name?:refresh=y", None) == "wb-name/sheets/view-name"

    """
    GetUrl.get_view(url)
    GetUrl.get_view_without_extension(view_name)
    GetUrl.get_workbook(url)
    """

    """
    GetUrl.generate_twb(logger, server, args)
    GetUrl.generate_pdf(logger, server, args)
    GetUrl.generate_png(logger, server, args)
    GetUrl.generate_csv(logger, server, args)
    """


@mock.patch("tableauserverclient.ViewItem", fake_item)
class ExportTests(unittest.TestCase):

    mock_logger = mock.MagicMock("logger")
    fake_item.csv = mock.MagicMock("bytes[]")
    fake_item.pdf = mock.MagicMock("bytes")
    fake_item.png = mock.MagicMock("bytes")

    def test_parse_export_url_to_workbook_and_view(self):
        wb_url = "wb-name/view-name"
        view, wb = ExportCommand.parse_export_url_to_workbook_and_view(mock_logger, wb_url)
        assert view == "wb-name/sheets/view-name"
        assert wb == "wb-name"

    def test_parse_export_url_to_workbook_and_view_with_start_slash(self):
        wb_url = "/wb-name/view-name"
        view, wb = ExportCommand.parse_export_url_to_workbook_and_view(mock_logger, wb_url)
        assert view == "wb-name/sheets/view-name"
        assert wb == "wb-name"

    def test_parse_export_url_to_workbook_and_view_bad_url(self):
        wb_url = "wb-name/view-name/kitty"
        view, wb = ExportCommand.parse_export_url_to_workbook_and_view(mock_logger, wb_url)
        assert view is None
        assert wb is None

    @mock.patch("tableauserverclient.Server")
    def test_download_csv(self, mock_server):
        mock_server.views = mock.MagicMock()
        mock_server.views.csv = mock.MagicMock()
        mock_view = tableauserverclient.ViewItem()
        url = "wb-name/view-name?param1=value1"
        mock_args.url = url
        ExportCommand.download_csv(mock_server, mock_view, mock_args, mock_logger)

    @mock.patch("tableauserverclient.Server")
    def test_download_image(self, mock_server):
        mock_server.views = mock.MagicMock()
        mock_server.views.png = mock.MagicMock()
        mock_view = tableauserverclient.ViewItem()
        url = "wb-name/view-name?param1=value1"
        mock_args.url = url
        ExportCommand.download_png(mock_server, mock_view, mock_args, mock_logger)

    @mock.patch("tableauserverclient.Server")
    def test_download_view_pdf(self, mock_server):
        mock_server.views = mock.MagicMock()
        mock_server.views.pdf = mock.MagicMock()
        mock_view = tableauserverclient.ViewItem()
        url = "wb-name/view-name?param1=value1"
        mock_args.url = url
        ExportCommand.download_view_pdf(mock_server, mock_view, mock_args, mock_logger)

    @mock.patch("tableauserverclient.Server")
    def test_download_wb_pdf(self, mock_server):
        mock_server.workbooks = mock.MagicMock()
        mock_server.workbooks.pdf = mock.MagicMock()
        mock_view = tableauserverclient.ViewItem()
        url = "wb-name/view-name?param1=value1"
        mock_args.url = url
        ExportCommand.download_wb_pdf(mock_server, mock_view, mock_args, mock_logger)


@mock.patch("tableauserverclient.ViewItem", fake_item)
class DS_WB_Tests(unittest.TestCase):
    def test_apply_filter(self):
        url = "wb-name/view-name?param1=value1"
        options = TSC.PDFRequestOptions()
        assert options.view_filters is not None
        assert len(options.view_filters) is 0
        ExportCommand.apply_filter_value(mock_logger, options, "param1=value1")
        assert len(options.view_filters) == 1
        assert options.view_filters[0] == ("param1", "value1")

    def test_extract_query_params(self):
        url = "wb-name/view-name?param1=value1"
        options = TSC.PDFRequestOptions()
        assert options.view_filters is not None
        assert len(options.view_filters) is 0
        ExportCommand.apply_values_from_url_params(mock_logger, options, url)
        assert len(options.view_filters) == 1
        assert options.view_filters[0] == ("param1", "value1")

    def test_refresh_true(self):
        url = "wb-name/view-name?:refresh=TRUE"
        options = TSC.PDFRequestOptions()
        assert options.max_age == -1
        ExportCommand.apply_values_from_url_params(mock_logger, options, url)
        assert options.max_age == 0

    def test_refresh_yes(self):
        url = "wb-name/view-name?:refresh=yes"
        options = TSC.PDFRequestOptions()
        assert options.max_age == -1
        ExportCommand.apply_values_from_url_params(mock_logger, options, url)
        assert options.max_age == 0

    def test_refresh_y(self):
        url = "wb-name/view-name?:refresh=y"
        options = TSC.PDFRequestOptions()
        assert options.max_age == -1
        ExportCommand.apply_values_from_url_params(mock_logger, options, url)
        assert options.max_age == 0

    def test_save_to_binary_file(self):
        mock_content = bytes()
        filename = "test_out.pdf"
        ExportCommand.save_to_file(mock_logger, mock_content, filename)

    def test_save_to_data_file(self):
        mock_content = mock.MagicMock()
        filename = "test_out.csv"
        ExportCommand.save_to_data_file(mock_logger, mock_content, filename)
