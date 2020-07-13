
import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import argparse
import os 
import sys
from ..pythontabcmd2.commands import delete_project_command
delete_project_command_class = delete_project_command.DeleteProjectCommand

class DeleteProjectCommandTest(unittest.TestCase):
    def test_command_create_project_1(self):
        with mock.patch.object(delete_project_command_class, 'delete_project', return_value="successfully deleted project"):
            delete_project_command_object = delete_project_command_class("testproject", None)
            assert delete_project_command_object.delete_project() == "successfully deleted project"
    
    def test_command_create_project_2(self):
            mock_server_obj = mock.Mock()
            test_project_name = "test_project"
            delete_project_command_object = delete_project_command_class("testproject", None)


if __name__ == "__main__":
    unittest.main()
