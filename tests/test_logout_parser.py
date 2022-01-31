import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd.parsers.logout_parser import LogoutParser


class LogoutParserTest(unittest.TestCase):

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
    def test_logout_username_password(self, mock_args):
        args = LogoutParser.logout_parser()
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
                return_value=argparse.Namespace())
    def test_logout_missing_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args = LogoutParser.logout_parser()
            assert args == argparse.Namespace()

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
    def test_logout_missing_server(self, mock_args):
        args = LogoutParser.logout_parser()
        assert args == argparse.Namespace(
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
                    site="",
                    logging_level="info",
                    password="testing123",
                    no_prompt=True, token=None,
                    token_name=None,
                    cookie=True,
                    no_cookie=False,
                    prompt=False
                ))
    def test_logout_missing_username(self, mock_args):
        args = LogoutParser.logout_parser()
        assert args == argparse.Namespace(
            site="",
            logging_level="info",
            password="testing123",
            no_prompt=True, token=None,
            token_name=None,
            cookie=True,
            no_cookie=False,
            prompt=False)
