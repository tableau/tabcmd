import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.runschedule_parser import RunScheduleParser


class RunScheduleParserTest(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    username="helloworld",
                    site="",
                    logging_level="info",
                    password="testing123",
                    no_prompt=True, token=None,
                    token_name=None,
                    cookie=True,
                    no_cookie=False,
                    prompt=False
                ))
    def test_runschedule_parser_optional_arguments(self, mock_args):
        args, schedule = RunScheduleParser.runschedule_parser()
        assert args == argparse.Namespace(username="helloworld",
                                          site="",
                                          logging_level="info",
                                          password="testing123",
                                          no_prompt=True, token=None,
                                          token_name=None,
                                          cookie=True,
                                          no_cookie=False,
                                          prompt=False)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_runschedule_parser_missing_all_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args, schedule = RunScheduleParser.runschedule_parser()
