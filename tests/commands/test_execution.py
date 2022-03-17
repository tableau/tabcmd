import argparse
import sys
import unittest
import mock

from tabcmd.execution.tabcmd_controller import TabcmdController


class ExecutionTests(unittest.TestCase):

    @mock.patch("sys.argv", [""])
    def test_run_e2e(self):
        parser = TabcmdController.initialize()
        TabcmdController.run(parser, ["help"])
            # check exit code = 0?

    def test_run_initialize(self):
        TabcmdController.initialize()

    @mock.patch("sys.argv", "")
    def test_run_inputs(self):
        fake_parser = mock.MagicMock(argparse.ArgumentParser)
        with self.assertRaises(SystemExit):
            TabcmdController.run(fake_parser, None)
