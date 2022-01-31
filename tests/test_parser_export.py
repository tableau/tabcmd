import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.export_parser import ExportParser


class ExportParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(url="helloworld", pdf=True,
                                                fullpdf=False, site=""))
    def test_export_parser_file_type_pdf(self, mock_args):
        url = "test"
        args, url = ExportParser.export_parser()
        assert args == argparse.Namespace(url="helloworld", pdf=True,
                                          fullpdf=False, site="")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(url="helloworld", pdf=False,
                                                fullpdf=True, site=""))
    def test_export_parser_missing_file_type_pdf(self, mock_args):
        args, url = ExportParser.export_parser()
        assert args == argparse.Namespace(url="helloworld", pdf=False,
                                          fullpdf=True, site="")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_export_parser_missing_all_args(self, mock_args):
        with self.assertRaises(Exception):
            args, url = ExportParser.export_parser()
