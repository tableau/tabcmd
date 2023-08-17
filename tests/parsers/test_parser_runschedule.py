import unittest

from tabcmd.commands.datasources_and_workbooks.runschedule_command import RunSchedule
from .common_setup import *

commandname = "runschedule"


class RunScheduleParserTest(ParserTestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, RunSchedule)

    def test_runschedule_parser_required_name(self):
        mock_args = [commandname, "schedulename"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.schedule == "schedulename"

    def test_runschedule_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(mock_args)
