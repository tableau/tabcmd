import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd2.parsers.export_parser import ExportParser


class ExportParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(pdf=True, fullpdf=True))
    def test_export_parser_file_type_pdf(self, mock_args):
        with self.assertRaises(AttributeError):
            args, url = ExportParser.export_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(pdf=True, fullpdf=False))
    def test_export_parser_file_type_fullpdf(self, mock_args):
        with self.assertRaises(AttributeError):
            args, url = ExportParser.export_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_export_parser_missing_all_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args, url = ExportParser.export_parser()

