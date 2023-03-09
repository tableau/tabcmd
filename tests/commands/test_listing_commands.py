import argparse
from unittest.mock import MagicMock

from tabcmd.commands.site.list_command import ListCommand
from tabcmd.commands.site.list_sites_command import ListSiteCommand

import unittest
from unittest import mock

mock_logger = mock.MagicMock()

fake_item = mock.MagicMock()
fake_item.name = "fake-name"
fake_item.id = "fake-id"
fake_item.extract_encryption_mode = "ENFORCED"

getter = MagicMock()
getter.get = MagicMock("get", return_value=([fake_item], 1))

mock_args = argparse.Namespace()
mock_args.logging_level = "INFO"


@mock.patch("tabcmd.commands.auth.session.Session.create_session")
@mock.patch("tableauserverclient.Server")
class ListingTests(unittest.TestCase):
    def test_list_sites(self, mock_server, mock_session):
        mock_server.sites = getter
        mock_args.get_extract_encryption_mode = False
        mock_session.return_value = mock_server
        out_value = ListSiteCommand.run_command(mock_args)

    def test_list_content(self, mock_server, mock_session):
        mock_server.flows = getter
        mock_args.content = "flows"
        mock_session.return_value = mock_server
        out_value = ListCommand.run_command(mock_args)

    def test_list_wb_details(self, mock_server, mock_session):
        mock_server.workbooks = getter
        mock_args.content = "workbooks"
        mock_session.return_value = mock_server
        mock_args.details = True
        out_value = ListCommand.run_command(mock_args)

    def test_list_datasources(self, mock_server, mock_session):
        mock_server.datasources = getter
        mock_args.content = "datasources"
        mock_session.return_value = mock_server
        mock_args.details = True
        out_value = ListCommand.run_command(mock_args)

    def test_list_projects(self, mock_server, mock_session):
        mock_server.projects = getter
        mock_args.content = "projects"
        mock_session.return_value = mock_server
        mock_args.details = True
        out_value = ListCommand.run_command(mock_args)
