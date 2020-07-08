
import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import argparse
import os 
import sys
from ..pythontabcmd2.commands import create_project_command
create_project_command_class = create_project_command.CreateProjectCommand

class CreteProjectCommandTest(unittest.TestCase):
    def test_command_create_project(self):
        with mock.patch.object(create_project_command_class, 'create_project', return_value="successfully created project"):
            create_project_command_object = create_project_command_class("testproject", None, None, None)
            assert create_project_command_object.create_project() == "successfully created project"
            
if __name__ == "__main__":
    unittest.main()