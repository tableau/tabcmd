import unittest
from unittest import mock

import tableauserverclient

from tabcmd.commands.project.project_command import ProjectCommand
from tabcmd.execution.logger_config import log

fake_item = mock.MagicMock()
fake_item.name = "fake-name"
fake_item.id = "fake-id"
getter = mock.MagicMock("get", return_value=([fake_item], 1))


class ProjectsTest(unittest.TestCase):
    logger = log("Projects_Tests", "debug")

    @staticmethod
    def test_parent_path_to_list():
        assert ProjectCommand._parse_project_path_to_list(None) == []
        assert ProjectCommand._parse_project_path_to_list("") == [""]
        assert ProjectCommand._parse_project_path_to_list("parent") == ["parent"]
        assert ProjectCommand._parse_project_path_to_list("parent/child") == ["parent", "child"]

    @mock.patch("tableauserverclient.Server")
    def test_get_project(self, mock_server):
        mock_server.projects.get = getter
        ProjectCommand.get_project_by_name_and_parent_path(mock_server, "random_name", "")
        getter.assert_called()
