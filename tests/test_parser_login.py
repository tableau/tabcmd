import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.login_parser import LoginParser


class LoginParserTest(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    server="https://localhost/",
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
    def test_login_parser_test_username_password(self, mock_args):
        args = LoginParser.login_parser()
        assert args == argparse.Namespace(server="https://localhost/",
                                          username="helloworld",
                                          site="",
                                          logging_level="info",
                                          password="testing123",
                                          no_prompt=True, token=None,
                                          token_name=None,
                                          cookie=True,
                                          no_cookie=False,
                                          prompt=False)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    server="https://localhost/",
                    username=None,
                    site="",
                    logging_level="info",
                    password=None,
                    no_prompt=True, token=None,
                    token_name="test",
                    cookie=True,
                    no_cookie=False,
                    prompt=False))
    def test_login_parser_token_name(self, mock_args):
        with self.assertRaises(SystemExit):
            args = LoginParser.login_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    server="https://localhost/",
                    username="test",
                    site="",
                    logging_level="info",
                    password=None,
                    no_prompt=True, token=None,
                    token_name=None,
                    cookie=True,
                    no_cookie=False,
                    prompt=False))
    def test_login_parser_username_pass(self, mock_args):
        with self.assertRaises(SystemExit):
            args = LoginParser.login_parser()
