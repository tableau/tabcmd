import unittest
from unittest import mock
from tabcmd.commands.datasources_and_workbooks.get_url_command import *
from tabcmd.commands.datasources_and_workbooks.export_command import *
from tabcmd.commands.server import Server

mock_logger = mock.MagicMock()


class GeturlTests(unittest.TestCase):
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

    def test_get_workbook_name(self):
        assert GetUrl.get_workbook_name(mock_logger, "/workbooks/wbname") == "wbname"

    def test_view_name(self):
        assert GetUrl.get_view_url("/views/wb-name/view-name") == "wb-name/sheets/view-name"

    """
    GetUrl.get_view_without_extension(view_name)
    GetUrl.get_view(url)
    GetUrl.get_workbook(url)
    GetUrl.generate_twb(logger, server, args)
    GetUrl.generate_pdf(logger, server, args)
    GetUrl.generate_png(logger, server, args)
    GetUrl.generate_csv(logger, server, args)
    """


class ExportTests(unittest.TestCase):
    def test_parse_export_url_to_workbook(self):
        wb_url = "wb-name/view-name"
        view, wb = ExportCommand.parse_export_url_to_workbook_and_view(mock_logger, wb_url)
        assert view == "wb-name/sheets/view-name"
        assert wb == "wb-name"
