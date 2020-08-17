import sys
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd2.tabcmd2_controller import Tabcmd2Controller


class Tabcmd2ControllerTest(unittest.TestCase):

    @mock.patch.object(sys, 'argv',['', 'createproject','--name', 'testname'])
    @mock.patch('pythontabcmd2.commands.project.create_project_command'
                '.CreateProjectCommand')
    def test_parser_called_command_project(self, mock_args):
        dic = {'CreateProjectCommand': 'createproject'}
        tabcmd2_controller = Tabcmd2Controller()
        command = tabcmd2_controller.get_command_strategy()
        assert command == dic['CreateProjectCommand']


    @mock.patch.object(sys, 'argv',['', 'creategroup','--name', 'testname'])
    @mock.patch('pythontabcmd2.commands.group.create_group_command'
                '.CreateGroupCommand')
    def test_parser_called_command_group(self, mock_args):
        dic = {'CreateGroupCommand': 'creategroup'}
        tabcmd2_controller = Tabcmd2Controller()
        command = tabcmd2_controller.get_command_strategy()
        assert command == dic['CreateGroupCommand']