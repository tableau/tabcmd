import argparse
import sys
import unittest
import mock
from tabcmd.execution.logger_config import *
from tabcmd.execution.tabcmd_controller import TabcmdController


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

    def test_config_logger(self):
        configure_log("log_name", "DEBUG")
        configure_log("log_name", "INFO")
        configure_log("log_name", "ERROR")

    def test_get_logger(self):
        log("testing", "DEBUG")
