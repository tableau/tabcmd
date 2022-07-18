import argparse
import unittest
from unittest import mock

from tabcmd.commands.auth.logout_command import LogoutCommand
from .common_setup import *

commandname = "logout"


class LogoutParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, LogoutCommand)

    # Logout doesn't take any arguments, so it's a good one to check all the global args on

    @mock.patch(
        "sys.argv",
        argparse.Namespace(
            server="https://localhost/",
            username="helloworld",
            site="",
            logging_level="info",
            password="testing123",
            no_prompt=True,
            token=None,
            token_name=None,
            cookie=True,
            no_cookie=False,
            prompt=False,
        ),
    )
    def test_logout_username_password(self):
        mock_args = [
            commandname,
            "--server",
            "the-server",
            "--site",
            "the-site",
            "--username",
            "me",
            "--no-certcheck",
            "-x",
            "proxyname",
        ]
        args = self.parser_under_test.parse_args(mock_args)

    def test_logout_missing_server(self):
        mock_args = [commandname, "--logging-level", "DEBUG", "--username", "me"]
        args = self.parser_under_test.parse_args(mock_args)
        assert not args.server, args
        assert args.logging_level == "DEBUG", args

    def test_logout_missing_username(self):
        mock_args = [commandname, "--server", "the-server"]
        args = self.parser_under_test.parse_args(mock_args)
