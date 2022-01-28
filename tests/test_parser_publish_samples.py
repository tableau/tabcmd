import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd2.parsers.publish_samples_parser import PublishSamplesParser


class PublishParserParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="helloworld"))
    def test_publish_samples_parser_name(self, mock_args):
        with self.assertRaises(AttributeError):
            args, path = PublishSamplesParser.publish_samples_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_publish_samples_parser_missing_all_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args, path = PublishSamplesParser.publish_samples_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site="default",
                                                name="helloworld",
                                                parent_project_path="parent",
                                                ))
    def test_publish_samples_parser_optional_args(self, mock_args):
        args, path = PublishSamplesParser.publish_samples_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        assert args_from_command == args_from_mock
