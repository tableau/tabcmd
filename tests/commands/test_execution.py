import argparse
import sys
import unittest
import mock
from src.execution.logger_config import *
from src.execution.tabcmd_controller import TabcmdController


class ExecutionTests(unittest.TestCase):
    @mock.patch("sys.argv", [""])
    def test_launch(self):
        parser = TabcmdController.initialize()
        TabcmdController.run(parser, ["help"])
        # check exit code = 0?

    def test_initialize(self):
        TabcmdController.initialize()

    @mock.patch("sys.argv", "")
    def test_inputs(self):
        fake_parser = mock.MagicMock(argparse.ArgumentParser)
        with self.assertRaises(SystemExit):
            TabcmdController.run(fake_parser, None)

    def test_invalid_command(self):
        parser = TabcmdController.initialize()
        # crashes out during parse_args
        with self.assertRaises(SystemExit):
            TabcmdController.run(parser, ["boo", "--language", "fr"])

    def test_launch_languages(self):
        parser = TabcmdController.initialize()
        # crashes out from list_sites.cmd
        with self.assertRaises(SystemExit):
            TabcmdController.run(parser, ["listsites", "--language", "fr"])

    def test_config_logger(self):
        configure_log("log_name", "DEBUG")
        configure_log("log_name", "INFO")
        configure_log("log_name", "ERROR")

    def test_get_logger(self):
        log("testing", "DEBUG")
