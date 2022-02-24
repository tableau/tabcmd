import unittest
from unittest import mock
from tabcmd.commands.datasources_and_workbooks.get_url_command import *


class GetURlTests(unittest.TestCase):
    def test_evaluate_file_name_pdf(self):
        mock_logger = mock.MagicMock()
        filename = "filename.pdf"
        url = None
        filetype = GetUrl.evaluate_file_name(mock_logger, filename, url)
        assert filetype == "pdf", filetype

    def test_evaluate_file_name_url(self):
        mock_logger = mock.MagicMock()
        filename = None
        url = "long-url-stuff-goes-here.pdf"
        filetype = GetUrl.evaluate_file_name(mock_logger, filename, url)
        assert filetype == "pdf", filetype

    """
    GetUrl.evaluate_file_name(logger, filename, url)
    GetUrl.check_if_extension_present(view_name)
    GetUrl.get_view_without_extension(view_name)
    GetUrl.get_view(url)
    GetUrl.get_workbook(url)
    GetUrl.generate_twb(logger, server, args)
    GetUrl.generate_pdf(logger, server, args)
    GetUrl.generate_png(logger, server, args)
    GetUrl.generate_csv(logger, server, args)
    """
