import unittest
from unittest.mock import MagicMock, patch
import tableauserverclient as TSC
from tabcmd.commands.server import Server

class TestServer(unittest.TestCase):

    @patch('tabcmd.commands.server.TSC.RequestOptions')
    @patch('tabcmd.commands.server.TSC.Filter')
    def test_get_items_by_name_returns_items(self, MockFilter, MockRequestOptions):
        logger = MagicMock()
        item_endpoint = MagicMock()
        item_name = "test_item"
        container = None

        pagination_item = MagicMock()
        pagination_item.total_available = 1
        pagination_item.page_number = 1
        pagination_item.page_size = 1

        item = MagicMock()
        item_endpoint.get.return_value = ([item], pagination_item)

        result = Server.get_items_by_name(logger, item_endpoint, item_name, container)

        self.assertEqual(result, [item])
        logger.debug.assert_called()
        item_endpoint.get.assert_called()

    @patch('tabcmd.commands.server.TSC.RequestOptions')
    @patch('tabcmd.commands.server.TSC.Filter')
    def test_get_items_by_name_no_items_found(self, MockFilter, MockRequestOptions):
        logger = MagicMock()
        item_endpoint = MagicMock()
        item_name = "test_item"
        container = None

        pagination_item = MagicMock()
        pagination_item.total_available = 0
        pagination_item.page_number = 1
        pagination_item.page_size = 1

        item_endpoint.get.return_value = ([], pagination_item)

        with self.assertRaises(TSC.ServerResponseError):
            Server.get_items_by_name(logger, item_endpoint, item_name, container)

        logger.debug.assert_called()
        item_endpoint.get.assert_called()

    @patch('tabcmd.commands.server.TSC.RequestOptions')
    @patch('tabcmd.commands.server.TSC.Filter')
    def test_get_items_by_name_with_container(self, MockFilter, MockRequestOptions):
        logger = MagicMock()
        item_endpoint = MagicMock()
        item_name = "test_item"
        container = MagicMock()
        container.id = "container_id"

        pagination_item = MagicMock()
        pagination_item.total_available = 1
        pagination_item.page_number = 1
        pagination_item.page_size = 1

        item = MagicMock()
        item.project_id = "container_id"
        item_endpoint.get.return_value = ([item], pagination_item)

        result = Server.get_items_by_name(logger, item_endpoint, item_name, container)

        self.assertEqual(result, [item])
        logger.debug.assert_called()
        item_endpoint.get.assert_called()

    @patch('tabcmd.commands.server.TSC.RequestOptions')
    @patch('tabcmd.commands.server.TSC.Filter')
    def test_get_items_by_name_with_container_no_match(self, MockFilter, MockRequestOptions):
        logger = MagicMock()
        item_endpoint = MagicMock()
        item_name = "test_item"
        container = MagicMock()
        container.id = "container_id"

        pagination_item = MagicMock()
        pagination_item.total_available = 1
        pagination_item.page_number = 1
        pagination_item.page_size = 1

        item = MagicMock()
        item.project_id = "different_container_id"
        item_endpoint.get.return_value = ([item], pagination_item)

        result = Server.get_items_by_name(logger, item_endpoint, item_name, container)

        self.assertEqual(result, [])
        logger.debug.assert_called()
        item_endpoint.get.assert_called()

    @patch('tabcmd.commands.server.TSC.RequestOptions')
    @patch('tabcmd.commands.server.TSC.Filter')
    def test_get_items_by_name_multiple_pages(self, MockFilter, MockRequestOptions):
        logger = MagicMock()
        item_endpoint = MagicMock()
        item_name = "test_item"
        container = None

        pagination_item_1 = MagicMock()
        pagination_item_1.total_available = 3
        pagination_item_1.page_number = 1
        pagination_item_1.page_size = 1

        pagination_item_2 = MagicMock()
        pagination_item_2.total_available = 3
        pagination_item_2.page_number = 2
        pagination_item_2.page_size = 1

        pagination_item_3 = MagicMock()
        pagination_item_3.total_available = 3
        pagination_item_3.page_number = 3
        pagination_item_3.page_size = 1

        item_1 = MagicMock()
        item_2 = MagicMock()
        item_3 = MagicMock()

        item_endpoint.get.side_effect = [
            ([item_1], pagination_item_1),
            ([item_2], pagination_item_2),
            ([item_3], pagination_item_3)
        ]

        result = Server.get_items_by_name(logger, item_endpoint, item_name, container)

        self.assertEqual(result, [item_1, item_2, item_3])
        self.assertEqual(item_endpoint.get.call_count, 3)
        logger.debug.assert_called()

    @patch('tabcmd.commands.server.TSC.RequestOptions')
    @patch('tabcmd.commands.server.TSC.Filter')
    def test_get_items_by_name_multiple_pages_with_container(self, MockFilter, MockRequestOptions):
        logger = MagicMock()
        item_endpoint = MagicMock()
        item_name = "test_item"
        container = MagicMock()
        container.id = "container_id"

        pagination_item_1 = MagicMock()
        pagination_item_1.total_available = 3
        pagination_item_1.page_number = 1
        pagination_item_1.page_size = 1

        pagination_item_2 = MagicMock()
        pagination_item_2.total_available = 3
        pagination_item_2.page_number = 2
        pagination_item_2.page_size = 1

        pagination_item_3 = MagicMock()
        pagination_item_3.total_available = 3
        pagination_item_3.page_number = 3
        pagination_item_3.page_size = 1

        item_1 = MagicMock()
        item_1.project_id = "container_id_1"
        item_2 = MagicMock()
        item_2.project_id = "container_id"
        item_3 = MagicMock()
        item_3.project_id = "container_id_2"

        item_endpoint.get.side_effect = [
            ([item_1], pagination_item_1),
            ([item_2], pagination_item_2),
            ([item_3], pagination_item_3)
        ]

        result = Server.get_items_by_name(logger, item_endpoint, item_name, container)

        self.assertEqual(result, [item_2])
        self.assertEqual(item_endpoint.get.call_count, 3)
        logger.debug.assert_called()

    @patch('tabcmd.commands.server.TSC.RequestOptions')
    @patch('tabcmd.commands.server.TSC.Filter')
    def test_get_items_by_name_multiple_pages_no_container_match(self, MockFilter, MockRequestOptions):
        logger = MagicMock()
        item_endpoint = MagicMock()
        item_name = "test_item"
        container = MagicMock()
        container.id = "container_id"

        pagination_item_1 = MagicMock()
        pagination_item_1.total_available = 3
        pagination_item_1.page_number = 1
        pagination_item_1.page_size = 1

        pagination_item_2 = MagicMock()
        pagination_item_2.total_available = 3
        pagination_item_2.page_number = 2
        pagination_item_2.page_size = 1

        pagination_item_3 = MagicMock()
        pagination_item_3.total_available = 3
        pagination_item_3.page_number = 3
        pagination_item_3.page_size = 1

        item_1 = MagicMock()
        item_1.project_id = "different_container_id_1"
        item_2 = MagicMock()
        item_2.project_id = "different_container_id_2"
        item_3 = MagicMock()
        item_3.project_id = "different_container_id_3"

        item_endpoint.get.side_effect = [
            ([item_1], pagination_item_1),
            ([item_2], pagination_item_2),
            ([item_3], pagination_item_3)
        ]

        result = Server.get_items_by_name(logger, item_endpoint, item_name, container)

        self.assertEqual(result, [])
        self.assertEqual(item_endpoint.get.call_count, 3)
        logger.debug.assert_called()