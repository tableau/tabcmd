import unittest
from unittest import skip

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

    def test_publish_parser_save_oauth(self):
        mock_args = [
            commandname,
            "filename.twbx",
            "--oauth-username",
            "user",
            "--save-oauth",
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.save_oauth is True, args
        assert args.oauth_username == "user", args

    def test_publish_parser_thumbnails(self):
        mock_args = [commandname, "filename.twbx", "--thumbnail-username"]  # no value for thumbnail-user
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

        mock_args = [commandname, "filename.twbx", "--thumbnail-username", "goofy"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.thumbnail_username == "goofy", args

    @skip("Not yet implemented")
    def test_publish_parser_thumbnail_group(self):
        mock_args = [commandname, "filename.twbx", "--thumbnail-group", "goofy"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.thumbnail_group == "goofy", args

    """
    append | replace | overwrite -> result
    --------
    true   | F/empty | F/empty   -> append
    true   | F/empty | true      -> ERROR
    true   | true    | F/empty   -> ERROR
    .... basically, replace == overwrite, append != r/o
    """

    def test_publish_parser_append_options(self):
        mock_args = [commandname, "filename.twbx", "--append"]
        args = self.parser_under_test.parse_args(mock_args)

    def test_publish_parser_replace_and_append(self):
        mock_args = [commandname, "filename.twbx", "--append", "--replace"]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_publish_parser_replace_options(self):
        mock_args = [commandname, "filename.twbx", "--overwrite"]
        args = self.parser_under_test.parse_args(mock_args)

        mock_args = [commandname, "filename.twbx", "--replace"]
        args = self.parser_under_test.parse_args(mock_args)

        mock_args = [commandname, "filename.twbx", "--replace", "--overwrite"]
        args = self.parser_under_test.parse_args(mock_args)

    def test_publish_parser_deprecated_options(self):
        # does nothing in new tabcmd, but shouldn't break anything
        mock_args = [commandname, "filename.twbx", "--disable-uploader"]
        args = self.parser_under_test.parse_args(mock_args)
        mock_args = [commandname, "filename.twbx", "--restart", "argument"]
        args = self.parser_under_test.parse_args(mock_args)

    def test_publish_parser_use_bridge_option(self):
        mock_args = [commandname, "filename.twbx", "--use-tableau-bridge"]
        args = self.parser_under_test.parse_args(mock_args)
