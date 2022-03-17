import unittest

import argparse
from tabcmd.parsers.login_parser import LoginParser
from common_setup import *

commandname = "login"


class LoginParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        LoginParser.login_parser(manager, mock_command)

    def test_login_parser_test_username_password(self):
        mock_args = [commandname, "--username", "helloworld", "--password", "pw"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.username == "helloworld", args
        assert args.password == "pw", args

    def test_login_parser_test_token(self):
        mock_args = [commandname, "--token", "token", "--token-name", "tn"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.token_name == "tn", args
        assert args.token == "token", args

    def test_login_token_and_username(self):
        mock_args = [commandname, "--token-name", "to", "--username", "u"]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
