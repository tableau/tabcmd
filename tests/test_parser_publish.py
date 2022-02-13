import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.publish_parser import PublishParser


class PublishParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="helloworld"))
    def test_publish_parser_missing_overwrite(self, mock_args):
        with self.assertRaises(AttributeError):
            args = PublishParser.publish_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_publish_parser_missing_all_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args = PublishParser.publish_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="testsite",
                                                project="helloworld",
                                                tabbed=True,
                                                site="helloworld",
                                                parent_project_path=None))
    def test_publish_parser_user_quota_integer(self, mock_args):
        args = PublishParser.publish_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        assert args_from_command == args_from_mock
