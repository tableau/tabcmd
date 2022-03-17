import unittest

import argparse
from tabcmd.parsers.runschedule_parser import RunScheduleParser
from common_setup import *


commandname = "runschedule"


class RunScheduleParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        RunScheduleParser.runschedule_parser(manager, mock_command)

    def test_runschedule_parser_required_name(self):
        mock_args = [commandname, "schedulename"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.schedule == "schedulename"

    def test_runschedule_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(mock_args)
