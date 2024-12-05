import argparse
from unittest.mock import MagicMock

from tabcmd.commands.datasources_and_workbooks.datasources_and_workbooks_command import DatasourcesAndWorkbooks
import tableauserverclient as tsc
import unittest
from unittest import mock

mock_logger = mock.MagicMock()

fake_item = mock.MagicMock()
fake_item.name = "fake-name"
fake_item.id = "fake-id"

getter = MagicMock()
getter.get = MagicMock("get", return_value=([fake_item], 1))
getter.get_by_id = MagicMock("get_by_id", return_value=([fake_item], 1))

mock_args = argparse.Namespace()


class ParameterTests(unittest.TestCase):
    def test_get_view_url_from_names(self):
        wb_name = "WB"
        view_name = "VIEW"
        out_value = DatasourcesAndWorkbooks.get_view_url_from_names(wb_name, view_name)
        assert out_value == "{}/sheets/{}".format(wb_name, view_name)

    def test_apply_filters_from_url_params(self):
        query_params = "?Product=widget"
        expected = [("Product", "widget")]
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, query_params)
        assert request_options.view_filters == expected

    def test_apply_encoded_filters_from_url_params(self):
        query_params = "?Product%20type=Z%C3%BCrich"
        expected = [("Product type", "Zürich")]
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, query_params)
        assert request_options.view_filters == expected

    def test_apply_options_from_url_params(self):
        query_params = "?:iid=5&:refresh=yes&:size=600,700"
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, query_params)
        assert request_options.max_age == 0

    def test_apply_png_options(self):
        # these aren't implemented yet. the layout and orientation ones don't apply.
        mock_args.width = 800
        mock_args.height = 76
        request_options = tsc.ImageRequestOptions()
        DatasourcesAndWorkbooks.apply_png_options(mock_logger, request_options, mock_args)
        assert request_options.image_resolution == "high"

    def test_apply_pdf_options(self):
        expected_page = tsc.PDFRequestOptions.PageType.Folio.__str__()
        expected_layout = tsc.PDFRequestOptions.Orientation.Portrait.__str__()
        mock_args.pagelayout = expected_layout
        mock_args.pagesize = expected_page
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_pdf_options(mock_logger, request_options, mock_args)
        assert request_options.page_type == expected_page
        assert request_options.orientation == expected_layout


@mock.patch("tableauserverclient.Server")
class MockedServerTests(unittest.TestCase):
    def test_mock_getter(self, mock_server):
        mock_server.fakes = getter
        mock_server.fakes.get()
        getter.get.assert_called()

    def test_get_ds_by_content_url(self, mock_server):
        mock_server.datasources = getter
        content_url = "blah"
        DatasourcesAndWorkbooks.get_ds_by_content_url(mock_logger, mock_server, content_url)
        getter.get.assert_called()
        # should also assert the filter on content url

    def test_get_wb_by_content_url(self, mock_server):
        mock_server.workbooks = getter
        content_url = "blah"
        DatasourcesAndWorkbooks.get_wb_by_content_url(mock_logger, mock_server, content_url)
        getter.get.assert_called()
        # should also assert the filter on content url

    def test_get_view_by_content_url(self, mock_server):
        mock_server.views = getter
        content_url = "blah"
        DatasourcesAndWorkbooks.get_view_by_content_url(mock_logger, mock_server, content_url)
        getter.get.assert_called()
        # should also assert the filter on content url

    def test_get_custom_view_by_id(self, mock_server):
        mock_server.custom_views = getter
        custom_view_id = "cv-id"
        DatasourcesAndWorkbooks.get_custom_view_by_id(mock_logger, mock_server, custom_view_id)
        getter.get_by_id.assert_called()
