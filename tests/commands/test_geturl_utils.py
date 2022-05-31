import unittest
from unittest import mock
from tabcmd.commands.datasources_and_workbooks.get_url_command import *
from tabcmd.commands.server import Server

mock_logger = mock.MagicMock()


class GetURlTests(unittest.TestCase):
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

    def test_check_for_extension_no_ext(self):
        filename = "workbook/viewname"
        filetype = GetUrl.get_file_extension(filename)
        assert not filetype

    def test_check_for_extension_twb(self):
        filename = "workbooks/viewname.twb"
        filetype = GetUrl.get_file_extension(filename)
        assert filetype == "twb", filetype

    def test_check_for_extension_twbx(self):
        filename = "workbooks/viewname.twbx"
        filetype = GetUrl.get_file_extension(filename)
        assert filetype == "twbx", filetype

    def test_check_for_extension_pdf(self):
        filename = "workbooks/workbook/viewname.pdf"
        filetype = GetUrl.get_file_extension(filename)
        assert filetype == "pdf", filetype

    """
    GetUrl.get_view_without_extension(view_name)
    GetUrl.get_view(url)
    GetUrl.get_workbook(url)
    GetUrl.generate_twb(logger, server, args)
    GetUrl.generate_pdf(logger, server, args)
    GetUrl.generate_png(logger, server, args)
    GetUrl.generate_csv(logger, server, args)
    """
