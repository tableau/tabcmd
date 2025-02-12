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

@mock.patch("tabcmd.commands.auth.session.Session.create_session")
@mock.patch("tableauserverclient.Server")
class ListingTests(unittest.TestCase):
    
    
    @staticmethod
    def _set_up_session(mock_session, mock_server):
        mock_session.return_value = mock_server
        assert mock_session is not None
        mock_session.assert_not_called()
        global mock_args
        mock_args = argparse.Namespace(logging_level="DEBUG")
        # set values for things that should always have a default
        # should refactor so this can be automated
        mock_args.continue_if_exists = False
        mock_args.project_name = None
        mock_args.parent_project_path = None
        mock_args.parent_path = None
        mock_args.timeout = None
        mock_args.username = None
        mock_args.name = True
        mock_args.owner = None
        mock_args.address = None
        mock_args.get_extract_encryption_mode = False
        mock_args.details = False
    
    
    def test_list_sites(self, mock_server, mock_session):
        ListingTests._set_up_session(mock_session, mock_server)
        mock_server.sites = getter
        out_value = ListSiteCommand.run_command(mock_args)

    def test_list_content(self, mock_server, mock_session):
        ListingTests._set_up_session(mock_session, mock_server)
        mock_server.flows = getter
        mock_args.content = "flows"
        out_value = ListCommand.run_command(mock_args)

    def test_list_wb_details(self, mock_server, mock_session):
        ListingTests._set_up_session(mock_session, mock_server)
        mock_server.workbooks = getter
        mock_args.content = "workbooks"
        mock_session.return_value = mock_server
        mock_args.details = True
        out_value = ListCommand.run_command(mock_args)

    def test_list_datasources(self, mock_server, mock_session):
        ListingTests._set_up_session(mock_session, mock_server)
        mock_server.datasources = getter
        mock_args.content = "datasources"
        mock_session.return_value = mock_server
        mock_args.details = True
        out_value = ListCommand.run_command(mock_args)

    def test_list_projects(self, mock_server, mock_session):
        ListingTests._set_up_session(mock_session, mock_server)
        mock_server.projects = getter
        mock_args.content = "projects"
        mock_session.return_value = mock_server
        mock_args.details = True
        out_value = ListCommand.run_command(mock_args)
