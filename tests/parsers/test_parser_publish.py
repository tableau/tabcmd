import unittest

from tabcmd.commands.datasources_and_workbooks.publish_command import PublishCommand
from .common_setup import *

commandname = "Publish"


class PublishParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, PublishCommand)

    def test_publish_parser_required_name(self):
        mock_args = [commandname, "filename.hyper"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.filename == "filename.hyper", args

    def test_publish_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_publish_parser_tabbed(self):
        mock_args = [commandname, "filename.twbx", "--tabbed"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.tabbed is True, args

    def test_publish_parser_save_password(self):
        mock_args = [
            commandname,
            "filename.twbx",
            "--db-username",
            "user",
            "--db-password",
            "somepassword",
            "--save-db-password",
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.save_db_password is True, args
