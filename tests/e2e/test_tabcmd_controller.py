import sys
import unittest
from unittest import mock
from tabcmd.execution.tabcmd_controller import TabcmdController


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

    @mock.patch.object(sys, 'argv', ['', 'creategroup', '--name', 'testname'])
    @mock.patch('tabcmd.commands.group.create_group_command'
                '.CreateGroupCommand')
    def test_parser_called_command_group(self, mock_args):
        dic = {'CreateGroupCommand': 'creategroup'}
        tabcmd_controller = TabcmdController()
        command = tabcmd_controller.get_command_strategy()
        assert command == dic['CreateGroupCommand']
