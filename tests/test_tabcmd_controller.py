import sys
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.tabcmd_controller import TabcmdController


class TabcmdControllerTest(unittest.TestCase):

    @mock.patch.object(sys, 'argv', ['', 'createproject', '--name',
                                     'testname'])
    @mock.patch('tabcmd.commands.project.create_project_command'
                '.CreateProjectCommand')
    def test_parser_called_command_project(self, mock_args):
        dic = {'CreateProjectCommand': 'createproject'}
        tabcmd_controller = TabcmdController()
        command = tabcmd_controller.get_command_strategy()
        assert command == dic['CreateProjectCommand']

