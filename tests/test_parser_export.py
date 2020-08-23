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
    def test_create_site_parser_missing_all_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args, url = ExportParser.export_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(pdf=True, png=True,
                                                csv=False,
                                                filename="helloworld",
                                                site="hello"))
    def test_create_site_parser_user_quota_integer(self, mock_args):
        args, url = ExportParser.export_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        assert args_from_command == args_from_mock
