import unittest
from unittest import mock
from tabcmd.parsers.login_parser import LoginParser
from .common_setup import *

commandname = "login"


@mock.patch("sys.argv", None)
class LoginParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        LoginParser.login_parser(manager, mock_command)

    def test_Login_username_password(self):
        mock_args = [
            commandname,
            "--server",
            "the-server",
            "--site",
            "the-site",
            "--username",
            "me",
            "--password",
            "the-password"
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.username == "me", args
        assert args.password == "the-password", args
        assert args.server == "the-server", args
        assert args.site == "the-site"

    def test_parsing_connection_settings(self):
        mock_args = [
            commandname,
            "--no-certcheck",
            "--proxy",
            "the-proxy",
            "--timeout",
            "10"
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.no_certcheck is True, args
        assert args.proxy == "the-proxy", args
        assert args.timeout == "10", args

    def test_parsing_no_proxy_no_cert(self):
        mock_args = [
            commandname,
            "--no-certcheck",
            "--no-proxy"
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.no_certcheck is True, args
        assert args.proxy is False, args

    def test_parsing_cert(self):
        mock_args = [
            commandname,
            "--use-certificate",
            "certificate-name"
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.no_certcheck is False, args
        assert args.certificate == "certificate-name"

    def test_parsing_conflicting_cert_args(self):
        mock_args = [
            commandname,
            "--no-certcheck",
            "-c",
            "cert-name"
        ]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_parsing_conflicting_proxy_args(self):
        mock_args = [
            commandname,
            "--no-proxy",
            "-x",
            "proxy-name"
        ]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_server_not_required(self):
        mock_args = [commandname, "--logging-level", "DEBUG", "--username", "me"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.server == "http://localhost", args
        assert args.logging_level == "DEBUG", args

    def test_username_not_required(self):
        mock_args = [commandname, "--server", "the-server"]
        args = self.parser_under_test.parse_args(mock_args)

    def test_token_username_conflict(self):
        mock_args = [commandname, "--username", "the-user", "--token-name", "a-token"]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_password_password_file_conflict(self):
        mock_args = [commandname, "--password", "the-pwd", "--password_file", "a-file-name"]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_version(self):
        mock_args = [commandname, "--version", "the-pwd", "--password_file", "a-file-name"]
        with self.assertRaises(SystemExit):
            # this runs an action and exits
            args = self.parser_under_test.parse_args(mock_args)