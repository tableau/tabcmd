import unittest
import uuid
from unittest import mock

import tableauserverclient

from tabcmd.commands.datasources_and_workbooks.get_url_command import *
from tabcmd.commands.datasources_and_workbooks.export_command import *
from tabcmd.commands.datasources_and_workbooks.datasources_workbooks_views_url_parser import *
from tabcmd.commands.server import Server

mock_args = argparse.Namespace()
mock_args.pagelayout = None
mock_args.pagesize = None
mock_args.image_resolution = None
mock_args.width = None
mock_args.height = None
mock_args.filename = None
mock_args.filter = None
mock_args.resolution = None
mock_args.language = None

mock_logger = mock.MagicMock()

fake_item = mock.MagicMock(TSC.ViewItem)
fake_item.name = "fake-name"
fake_item.id = "fake-id"

fake_cv_id = str(uuid.uuid4())
fake_cv_item = mock.MagicMock(TSC.CustomViewItem)
fake_cv_item.name = "custom-view-name"
fake_cv_item.id = fake_cv_id
fake_cv_item.view.id = fake_item.id


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
        filetype = DatasourcesWorkbooksAndViewsUrlParser.get_file_type_from_filename(mock_logger, filename, url)
        assert filetype == "twbx", filetype

    def test_evaluate_file_name_pdf(self):
        filename = "filename.pdf"
        url = None
        filetype = DatasourcesWorkbooksAndViewsUrlParser.get_file_type_from_filename(mock_logger, filename, url)
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
        assert DatasourcesWorkbooksAndViewsUrlParser.get_name_without_possible_extension(filename) == "viewname"

    def test_get_view_without_extension_that_doesnt_have_one(self):
        filename = "viewname"
        assert DatasourcesWorkbooksAndViewsUrlParser.get_name_without_possible_extension(filename) == filename


# handling our specific url-ish identifiers: /workbook/wb-name, etc
class GeturlTests(unittest.TestCase):
    def test_get_workbook_name(self):
        assert DatasourcesWorkbooksAndViewsUrlParser.get_resource_name("workbooks/wbname", mock_logger) == "wbname"

    def test_view_name(self):
        assert (
            DatasourcesWorkbooksAndViewsUrlParser.get_view_url_from_get_url(mock_logger, "views/wb-name/view-name")
            == "wb-name/sheets/view-name"
        )

    def test_view_name_with_url_params(self):
        assert (
            DatasourcesWorkbooksAndViewsUrlParser.get_view_url_from_get_url(
                mock_logger, "views/wb-name/view-name?:refresh=y"
            )
            == "wb-name/sheets/view-name"
        )

    def test_get_url_parts_from_custom_view_url(self):
        cv_uuid = str(uuid.uuid4())
        custom_view_url = "views/wb-name/view-name/" + cv_uuid + "/custom-view-name"
        (
            view_url,
            custom_view_id,
            custom_view_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.get_custom_view_parts_from_get_url(mock_logger, custom_view_url)
        assert view_url == "wb-name/sheets/view-name"
        assert custom_view_id == cv_uuid
        assert custom_view_name == "custom-view-name"

    def test_get_url_parts_from_custom_view_url_invalid_cv_id(self):
        custom_view_url = "views/wb-name/view-name/cv_uuid/custom-view-name"
        with self.assertRaises(SystemExit):
            DatasourcesWorkbooksAndViewsUrlParser.get_custom_view_parts_from_get_url(mock_logger, custom_view_url)

    def test_get_url_parts_from_custom_view_url_bad_url(self):
        custom_view_url = "views/wb-name/view-name/cv_uuid/custom-view-name/kitty"
        with self.assertRaises(SystemExit):
            DatasourcesWorkbooksAndViewsUrlParser.get_custom_view_parts_from_get_url(mock_logger, custom_view_url)

    def test_get_url_parts_from_custom_view_url_with_url_params(self):
        cv_uuid = str(uuid.uuid4())
        custom_view_url = "views/wb-name/view-name/" + cv_uuid + "/custom-view-name?:refresh=yes"
        (
            view_url,
            custom_view_id,
            custom_view_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.get_custom_view_parts_from_get_url(mock_logger, custom_view_url)
        assert view_url == "wb-name/sheets/view-name"
        assert custom_view_id == cv_uuid
        assert custom_view_name == "custom-view-name"

    def test_get_url_parts_from_custom_view_url_with_file_extension(self):
        cv_uuid = str(uuid.uuid4())
        custom_view_url = "views/wb-name/view-name/" + cv_uuid + "/custom-view-name.png"
        (
            view_url,
            custom_view_id,
            custom_view_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.get_custom_view_parts_from_get_url(mock_logger, custom_view_url)
        assert view_url == "wb-name/sheets/view-name"
        assert custom_view_id == cv_uuid
        assert custom_view_name == "custom-view-name"

    def test_parse_get_url_to_view_parts(self):
        url = "views/wb-name/view-name"
        (
            view_url,
            cv_id,
            cv_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.parse_get_view_url_to_view_and_custom_view_parts(mock_logger, url)
        assert view_url == "wb-name/sheets/view-name"
        assert cv_id is None
        assert cv_name is None

    def test_parse_get_url_to_view_parts_with_params(self):
        url = "views/wb-name/view-name?params=1"
        (
            view_url,
            cv_id,
            cv_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.parse_get_view_url_to_view_and_custom_view_parts(mock_logger, url)
        assert view_url == "wb-name/sheets/view-name"
        assert cv_id is None
        assert cv_name is None

    def test_parse_get_url_to_view_parts_with_spaces(self):
        url = "views/wb name/view-name"
        with self.assertRaises(SystemExit):
            DatasourcesWorkbooksAndViewsUrlParser.parse_get_view_url_to_view_and_custom_view_parts(mock_logger, url)

    def test_parse_get_url_to_view_parts_without_slashes(self):
        url = "views\wb name\\view-name"
        with self.assertRaises(SystemExit):
            DatasourcesWorkbooksAndViewsUrlParser.parse_get_view_url_to_view_and_custom_view_parts(mock_logger, url)

    def test_parse_get_url_to_custom_view_parts(self):
        cv_uuid = str(uuid.uuid4())
        custom_view_url = "views/wb-name/view-name/" + cv_uuid + "/custom-view-name"
        (
            view_url,
            custom_view_id,
            custom_view_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.parse_get_view_url_to_view_and_custom_view_parts(
            mock_logger, custom_view_url
        )
        assert view_url == "wb-name/sheets/view-name"
        assert custom_view_id == cv_uuid
        assert custom_view_name == "custom-view-name"

    def test_parse_get_url_to_custom_view_parts_with_file_extension(self):
        cv_uuid = str(uuid.uuid4())
        custom_view_url = "views/wb-name/view-name/" + cv_uuid + "/custom-view-name.png"
        (
            view_url,
            custom_view_id,
            custom_view_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.parse_get_view_url_to_view_and_custom_view_parts(
            mock_logger, custom_view_url
        )
        assert view_url == "wb-name/sheets/view-name"
        assert custom_view_id == cv_uuid
        assert custom_view_name == "custom-view-name"

    @mock.patch("tableauserverclient.Server")
    def test_get_url_item_and_item_type_from_view_url(self, mock_server):
        view_url = "views/wb-name/view-name"
        mock_server.views = mock.MagicMock()
        mock_server.views.get = mock.MagicMock("get", return_value=([fake_item], 1))
        view_item, server_content_type = DatasourcesWorkbooksAndViewsUrlParser.get_url_item_and_item_type_from_view_url(
            mock_logger, view_url, mock_server
        )
        assert view_item == fake_item
        assert server_content_type == mock_server.views

    @mock.patch("tableauserverclient.Server")
    def test_get_url_item_and_item_type_from_custom_view_url(self, mock_server):
        view_url = "views/wb-name/view-name/" + fake_cv_id + "/custom-view-name"
        mock_server.views = mock.MagicMock()
        mock_server.views.get = mock.MagicMock("get", return_value=([fake_item], 1))
        mock_server.custom_views = mock.MagicMock()
        mock_server.custom_views.get_by_id = mock.MagicMock("get_by_id", return_value=fake_cv_item)
        cv_item, server_content_type = DatasourcesWorkbooksAndViewsUrlParser.get_url_item_and_item_type_from_view_url(
            mock_logger, view_url, mock_server
        )
        assert cv_item == fake_cv_item
        assert server_content_type == mock_server.custom_views

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

    def test_parse_export_url_to_workbook_view_and_custom_view(self):
        wb_url = "wb-name/view-name"
        (
            view,
            wb,
            cv_id,
            cv_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.parse_export_url_to_workbook_view_and_custom_view(mock_logger, wb_url)
        assert view == "wb-name/sheets/view-name"
        assert wb == "wb-name"
        assert cv_id is None
        assert cv_name is None

    def test_parse_export_url_to_workbook_view_and_custom_view_with_start_slash(self):
        wb_url = "/wb-name/view-name"
        (
            view,
            wb,
            cv_id,
            cv_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.parse_export_url_to_workbook_view_and_custom_view(mock_logger, wb_url)
        assert view == "wb-name/sheets/view-name"
        assert wb == "wb-name"
        assert cv_id is None
        assert cv_name is None

    def test_parse_export_url_to_workbook_view_and_custom_view_bad_url(self):
        wb_url = "wb-name/view-name/kitty"
        (
            view,
            wb,
            cv_id,
            cv_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.parse_export_url_to_workbook_view_and_custom_view(mock_logger, wb_url)
        assert view is None
        assert wb is None
        assert cv_id is None
        assert cv_name is None

    def test_parse_export_url_to_workbook_view_and_custom_view_with_cv_parts(self):
        cv_uuid = str(uuid.uuid4())
        custom_view_name = "custom-view-name"
        wb_url = "/wb-name/view-name/" + cv_uuid + "/" + custom_view_name
        (
            view,
            wb,
            cv_id,
            cv_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.parse_export_url_to_workbook_view_and_custom_view(mock_logger, wb_url)
        assert view == "wb-name/sheets/view-name"
        assert wb == "wb-name"
        assert cv_id == cv_uuid
        assert cv_name == custom_view_name

    def test_parse_export_url_to_workbook_view_and_custom_view_with_bad_cv_parts(self):
        cv_uuid = str(uuid.uuid4())
        custom_view_name = "custom-view-name"
        wb_url = "/wb-name/view-name/" + cv_uuid + "/" + custom_view_name + "/kitty"
        (
            view,
            wb,
            cv_id,
            cv_name,
        ) = DatasourcesWorkbooksAndViewsUrlParser.parse_export_url_to_workbook_view_and_custom_view(mock_logger, wb_url)
        assert view is None
        assert wb is None
        assert cv_id is None
        assert cv_name is None

    def test_parse_export_url_to_workbook_view_and_custom_view_with_invalid_cv_id(self):
        wb_url = "/wb-name/view-name/cv-id/cv-name"
        with self.assertRaises(SystemExit):
            DatasourcesWorkbooksAndViewsUrlParser.parse_export_url_to_workbook_view_and_custom_view(mock_logger, wb_url)

    @mock.patch("tableauserverclient.Server")
    def test_get_export_item_and_item_type_for_view(self, mock_server):
        view_url = "wb-name/sheets/view-name"
        mock_server.views = mock.MagicMock()
        mock_server.views.get = mock.MagicMock("get", return_value=([fake_item], 1))
        (
            view_item,
            server_content_type,
        ) = DatasourcesWorkbooksAndViewsUrlParser.get_export_item_and_server_content_type_from_export_url(
            view_url, mock_logger, mock_server, None
        )
        assert view_item == fake_item
        assert server_content_type == mock_server.views

    @mock.patch("tableauserverclient.Server")
    def test_get_export_item_and_item_type_for_custom_view(self, mock_server):
        view_url = "wb-name/sheets/view-name"
        mock_server.views = mock.MagicMock()
        mock_server.views.get = mock.MagicMock("get", return_value=([fake_item], 1))
        mock_server.custom_views = mock.MagicMock()
        mock_server.custom_views.get_by_id = mock.MagicMock("get_by_id", return_value=fake_cv_item)
        (
            cv_item,
            server_content_type,
        ) = DatasourcesWorkbooksAndViewsUrlParser.get_export_item_and_server_content_type_from_export_url(
            view_url, mock_logger, mock_server, fake_cv_id
        )
        assert cv_item == fake_cv_item
        assert server_content_type == mock_server.custom_views

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
