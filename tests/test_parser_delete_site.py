import sys
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.delete_site_parser import DeleteSiteParser


class DeleteSiteParserTest(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site_name="helloworld",
                                                username="test",
                                                password="testpass",
                                                server="http://test",
                                                site="helloworld"))
    def test_delete_site(self, mock_args):
        args = DeleteSiteParser.delete_site_parser()
        assert args == mock_args.return_value

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                                                username="test",
                                                password="testpass",
                                                server="http://test",
                                                site="helloworld"))
    def test_delete_site_required_name_none(self, mock_args):
        with self.assertRaises(AttributeError):
            args = DeleteSiteParser.delete_site_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_delete_site_missing_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args = DeleteSiteParser.delete_site_parser()
