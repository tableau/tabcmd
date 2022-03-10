import unittest
from unittest import mock
from tabcmd.commands.datasources_and_workbooks.get_url_command import *
from tabcmd.commands.commands import Commands

mock_logger = mock.MagicMock()


class GetURlTests(unittest.TestCase):
    def test_evaluate_file_name_pdf(self):
        filename = "filename.pdf"
        url = None
        filetype = GetUrl.evaluate_file_name(mock_logger, filename, url)
        assert filetype == "pdf", filetype

    def test_evaluate_file_name_url(self):
        filename = "filename.twbx"
        filetype = Commands.get_filename_extension_if_tableau_type(mock_logger, filename)
        assert filetype == "twbx", filetype

    def test_evaluate_file_path(self):
        filename = "../assets/filename.twb"
        filetype = Commands.get_filename_extension_if_tableau_type(mock_logger, filename)
        assert filetype == "twb", filetype

    def test_evaluate_file_name_url_pdf_fails(self):
        filename = "filename.pdf"
        with self.assertRaises(ValueError):
            filetype = Commands.get_filename_extension_if_tableau_type(mock_logger, filename)

    def test_evaluate_file_name_url_no_ext_fails(self):
        filename = "filename/filename/filename/file"
        with self.assertRaises(ValueError):
            filetype = Commands.get_filename_extension_if_tableau_type(mock_logger, filename)

    def test_check_for_extension_no_ext(self):
        filename = "project/workbook/viewname"
        filetype = GetUrl.check_if_extension_present(filename)
        assert filetype is False

    def test_check_for_extension_twb(self):
        filename = "project/workbook/viewname.twb"
        filetype = GetUrl.check_if_extension_present(filename)
        assert filetype is True

    def test_check_for_extension_no_ext(self):
        filename = "workbooks/workbook/viewname.pdf"
        filetype = GetUrl.check_if_extension_present(filename)
        assert filetype is True

    """
    GetUrl.get_view_without_extension(view_name)
    GetUrl.get_view(url)
    GetUrl.get_workbook(url)
    GetUrl.generate_twb(logger, server, args)
    GetUrl.generate_pdf(logger, server, args)
    GetUrl.generate_png(logger, server, args)
    GetUrl.generate_csv(logger, server, args)
    """
