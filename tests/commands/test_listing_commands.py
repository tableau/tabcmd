import argparse
from unittest.mock import MagicMock, patch
import io
import sys

from tabcmd.commands.site.list_command import ListCommand
from tabcmd.commands.site.list_sites_command import ListSiteCommand
from tabcmd.execution.localize import set_client_locale

import unittest
from unittest import mock

mock_logger = mock.MagicMock()

fake_item = mock.MagicMock()
fake_item.name = "fake-name"
fake_item.id = "fake-id"
fake_item.extract_encryption_mode = "ENFORCED"
fake_item.owner_id = "fake-owner"
fake_item.content_url = "fake-url"

fake_view = mock.MagicMock()
fake_view.name = "fake-view"

getter = MagicMock()
getter.get = MagicMock("get", return_value=([fake_item], 1))
getter.all = MagicMock("all", return_value=[fake_item])


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
        mock_args.machine = False
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
        mock_server.workbooks.populate_views = MagicMock()
        fake_item.views = [fake_view]
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


class ListCommandFunctionalTests(unittest.TestCase):
    """Test that ListCommand properly uses localized strings in different scenarios"""

    @patch("tabcmd.commands.site.list_command._")
    @patch("tabcmd.commands.auth.session.Session")
    @patch("tabcmd.execution.logger_config.log")
    def test_show_header_with_all_options(self, mock_log, mock_session, mock_translate):
        """Test header generation with all display options enabled"""
        # Mock the translation function to return the actual English strings
        def translate_side_effect(key):
            translations = {
                "tabcmd.listing.header.id": "ID",
                "tabcmd.listing.header.name": "NAME",
                "tabcmd.listing.header.owner": "OWNER",
                "tabcmd.listing.header.url": "URL",
                "tabcmd.listing.header.children": "CHILDREN",
            }
            return translations.get(key, key)

        mock_translate.side_effect = translate_side_effect

        mock_args = argparse.Namespace(name=True, owner=True, address=True, details=True)

        # Test workbooks (should include all headers)
        header = ListCommand.show_header(mock_args, "workbooks")
        self.assertIn("ID", header)
        self.assertIn("NAME", header)
        self.assertIn("OWNER", header)
        self.assertIn("URL", header)
        self.assertIn("CHILDREN", header)

        # Test datasources (should include URL but not CHILDREN)
        header = ListCommand.show_header(mock_args, "datasources")
        self.assertIn("ID", header)
        self.assertIn("NAME", header)
        self.assertIn("OWNER", header)
        self.assertIn("URL", header)
        self.assertNotIn("CHILDREN", header)

        # Test projects (should not include URL or CHILDREN)
        header = ListCommand.show_header(mock_args, "projects")
        self.assertIn("ID", header)
        self.assertIn("NAME", header)
        self.assertIn("OWNER", header)
        self.assertNotIn("URL", header)
        self.assertNotIn("CHILDREN", header)

    @patch("tabcmd.commands.site.list_command._")
    @patch("tabcmd.commands.auth.session.Session")
    @patch("tabcmd.execution.logger_config.log")
    def test_show_header_minimal_options(self, mock_log, mock_session, mock_translate):
        """Test header generation with minimal options"""
        # Mock the translation function
        mock_translate.return_value = "ID"

        mock_args = argparse.Namespace(name=False, owner=False, address=False, details=False)

        header = ListCommand.show_header(mock_args, "workbooks")
        self.assertEqual(header, "ID")

    @patch("tabcmd.commands.site.list_command._")
    @patch("tableauserverclient.Server")
    def test_format_children_listing_workbooks(self, mock_server, mock_translate):
        """Test children listing format for workbooks"""
        # Mock the translation function
        mock_translate.return_value = "VIEWS: ["

        mock_args = argparse.Namespace(details=True)

        # Mock workbook item with views - create proper mock objects with string names
        view1 = MagicMock()
        view1.name = "View1"
        view2 = MagicMock()
        view2.name = "View2"

        mock_item = MagicMock()
        mock_item.views = [view1, view2]

        # Mock server populate_views method
        mock_server.workbooks.populate_views = MagicMock()

        result = ListCommand.format_children_listing(mock_args, mock_server, "workbooks", mock_item)

        self.assertIn("VIEWS: ", result)
        self.assertIn("View1", result)
        self.assertIn("View2", result)
        mock_server.workbooks.populate_views.assert_called_once_with(mock_item)

    @patch("tableauserverclient.Server")
    def test_format_children_listing_non_workbooks(self, mock_server):
        """Test children listing returns empty for non-workbook content types"""
        mock_args = argparse.Namespace(details=True)
        mock_item = MagicMock()

        result = ListCommand.format_children_listing(mock_args, mock_server, "datasources", mock_item)
        self.assertEqual(result, "")

        result = ListCommand.format_children_listing(mock_args, mock_server, "projects", mock_item)
        self.assertEqual(result, "")

    @patch("tableauserverclient.Server")
    def test_format_children_listing_no_details(self, mock_server):
        """Test children listing returns empty when details=False"""
        mock_args = argparse.Namespace(details=False)
        mock_item = MagicMock()

        result = ListCommand.format_children_listing(mock_args, mock_server, "workbooks", mock_item)
        self.assertEqual(result, "")


class LocalizedStringKeysTests(unittest.TestCase):
    """Test that ListCommand calls the correct localization keys"""

    @patch("tabcmd.commands.site.list_command._")
    def test_show_header_datasources_with_url(self, mock_translate):
        """Test that datasources headers include URL when address=True"""
        mock_translate.return_value = "TRANSLATED"

        mock_args = argparse.Namespace(
            name=True, owner=True, address=True, details=True  # With address=True, datasources should show URL
        )

        ListCommand.show_header(mock_args, "datasources")

        # Verify that URL key IS called for datasources (but not CHILDREN)
        expected_calls = [
            mock.call("tabcmd.listing.header.id"),
            mock.call("tabcmd.listing.header.name"),
            mock.call("tabcmd.listing.header.owner"),
            mock.call("tabcmd.listing.header.url"),  # Should be called for datasources too
            # Note: tabcmd.listing.header.children should NOT be called (only for workbooks)
        ]
        mock_translate.assert_has_calls(expected_calls, any_order=True)

        # Verify CHILDREN key was not called (only for workbooks)
        all_calls = [call[0][0] for call in mock_translate.call_args_list]
        self.assertNotIn("tabcmd.listing.header.children", all_calls)

    def test_show_header_structure_without_mocking(self):
        """Test the basic structure of show_header without mocking translations"""
        mock_args = argparse.Namespace(name=False, owner=False, address=False, details=False)

        # This should return just the ID header (even if it's the localization key)
        header = ListCommand.show_header(mock_args, "workbooks")

        # The result should be a single string (not contain commas when no options are set)
        self.assertNotIn(",", header)
        self.assertTrue(isinstance(header, str))
        self.assertGreater(len(header), 0)
