import unittest
from unittest import mock

from tabcmd.commands.auth.login_command import LoginCommand
from .common_setup import *

commandname: str = "login"


@mock.patch("sys.argv", None)
class GlobalOptionsPositionTest(ParserTest):
    """Global options must mean the same thing before and after the subcommand."""

    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, LoginCommand)

    def test_global_options_before_command_are_kept(self):
        args = self.parser_under_test.parse_args(
            ["--server", "the-server", "--site", "the-site", "--token-name", "n", "--language", "de", commandname]
        )
        assert args.server == "the-server", args
        assert args.site_name == "the-site", args
        assert args.token_name == "n", args
        assert args.language == "de", args

    def test_global_options_after_command_are_kept(self):
        args = self.parser_under_test.parse_args(
            [commandname, "--server", "the-server", "--site", "the-site", "--token-name", "n", "--language", "de"]
        )
        assert args.server == "the-server", args
        assert args.site_name == "the-site", args
        assert args.token_name == "n", args
        assert args.language == "de", args

    def test_option_after_command_wins_over_option_before(self):
        args = self.parser_under_test.parse_args(["--server", "first", commandname, "--server", "second"])
        assert args.server == "second", args

    def test_defaults_apply_when_option_not_given(self):
        args = self.parser_under_test.parse_args([commandname])
        assert args.server is None, args
        assert args.language is None, args
        assert args.site_name == "", args
        assert args.logging_level == "INFO", args


if __name__ == "__main__":
    unittest.main()
