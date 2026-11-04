import unittest

from tabcmd.commands.datasources_and_workbooks.export_command import ExportCommand
from .common_setup import *

commandname = "export"


class ExportParserTest(ParserTest):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, ExportCommand)

    def test_export_parser_file_type_pdf(self):
        mock_args = mock_args = ["export", "helloworld", "--pdf"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.pdf is True, args
        assert args.url == "helloworld", args

    def test_export_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_export_parser_country_normalized_to_upper(self):
        args = self.parser_under_test.parse_args(
            ["export", "helloworld", "--pdf", "--language", "en", "--country", "gb"]
        )
        assert args.country == "GB", args
        assert args.language == "en", args

    def test_export_parser_country_invalid_rejected(self):
        for bad in ["USA", "1", "gb-eng", "g", "", "é1"]:
            with self.subTest(country=bad):
                with self.assertRaises(SystemExit):
                    self.parser_under_test.parse_args(
                        ["export", "helloworld", "--pdf", "--language", "en", "--country", bad]
                    )

    def test_export_parser_single_filter(self):
        args = self.parser_under_test.parse_args([commandname, "helloworld", "--pdf", "--filter", "Region=West"])
        assert args.filter == ["Region=West"]

    def test_export_parser_repeated_filter(self):
        args = self.parser_under_test.parse_args(
            [commandname, "helloworld", "--pdf", "--filter", "Region=West", "--filter", "Product=AT&T"]
        )
        assert args.filter == ["Region=West", "Product=AT&T"]

    def test_export_parser_no_filter_defaults_to_none(self):
        args = self.parser_under_test.parse_args([commandname, "helloworld", "--pdf"])
        assert args.filter is None
