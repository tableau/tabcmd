import argparse
import unittest
from unittest import mock

from tabcmd.commands.auth.login_command import LoginCommand
from tabcmd.execution.parent_parser import ParentParser, parent_parser_with_global_options
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


# every global option, with a value where it takes one; each must mean the same thing in either position
GLOBAL_OPTIONS = [
    ["-s", "the-server"],
    ["-t", "the-site"],
    ["-u", "the-user"],
    ["--token-name", "the-token-name"],
    ["-p", "the-password"],
    ["--token-value", "the-token-value"],
    ["--password-file", "the-file"],
    ["--token-file", "the-file"],
    ["--no-prompt"],
    ["-c", "the-cert"],
    ["--no-certcheck"],
    ["--no-cookie"],
    ["-x", "host:1"],
    ["--no-proxy"],
    ["--timeout", "30"],
    ["--continue-if-exists"],
    ["--country", "DE"],
    ["--language", "DE"],
    ["-l", "debug"],
    ["--query-page-size", "5"],
]

# commands that parse with the given arguments and nothing else
COMMANDS = [["login"], ["logout"], ["listsites"], ["get", "/views/a/b"], ["creategroup", "the-group"]]


def real_parser() -> argparse.ArgumentParser:
    manager = ParentParser()
    manager.connect_commands()
    manager.include_help()
    return manager.get_root_parser()


def parse(parser: argparse.ArgumentParser, args: list) -> dict:
    values = vars(parser.parse_args(args))
    values.pop("func")
    return values


class GlobalOptionsRealCommandsTest(unittest.TestCase):
    """The same checks against the parser the CLI builds, not a single mocked command."""

    parser: argparse.ArgumentParser

    @classmethod
    def setUpClass(cls):
        cls.parser = real_parser()

    def test_every_global_option_means_the_same_before_and_after_the_command(self):
        for command in COMMANDS:
            defaults = parse(self.parser, command)
            for option in GLOBAL_OPTIONS:
                with self.subTest(command=command[0], option=option):
                    before = parse(self.parser, option + command)
                    after = parse(self.parser, command + option)
                    assert before == after, (before, after)
                    assert before != defaults, "{} had no effect".format(option)

    def test_option_values_before_the_command_are_converted(self):
        values = parse(
            self.parser, ["-l", "debug", "--language", "DE", "--country", "FR", "--query-page-size", "5", "login"]
        )
        assert values["logging_level"] == "DEBUG", values
        assert values["language"] == "de", values
        assert values["country"] == "fr", values
        assert values["query_page_size"] == 5, values

    def test_boolean_flags_default_to_false_and_are_kept_before_the_command(self):
        flags = {
            "--no-prompt": "no_prompt",
            "--no-certcheck": "no_certcheck",
            "--no-cookie": "no_cookie",
            "--no-proxy": "no_proxy",
            "--continue-if-exists": "continue_if_exists",
        }
        defaults = parse(self.parser, ["login"])
        for flag, name in flags.items():
            with self.subTest(flag=flag):
                assert defaults[name] is False, defaults
                assert parse(self.parser, [flag, "login"])[name] is True

    def test_every_global_default_is_present_for_every_command(self):
        expected = {a.dest for a in parent_parser_with_global_options()._actions if a.default is not argparse.SUPPRESS}
        assert len(expected) >= 19, expected
        for command in COMMANDS:
            with self.subTest(command=command[0]):
                missing = expected - set(parse(self.parser, command))
                assert not missing, missing

    def test_help_command_accepts_global_options_in_either_position(self):
        defaults = parse(self.parser, ["help"])
        assert defaults["server"] is None, defaults
        assert defaults["logging_level"] == "INFO", defaults
        assert parse(self.parser, ["-s", "the-server", "help"])["server"] == "the-server"
        assert parse(self.parser, ["help", "-s", "the-server"])["server"] == "the-server"


if __name__ == "__main__":
    unittest.main()
