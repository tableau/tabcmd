import logging
import logging.handlers
import unittest

from tabcmd.execution.logger_config import configure_log


class LoggerConfigTests(unittest.TestCase):
    def setUp(self):
        # Remove all handlers from root logger before each test to avoid
        # cross-test pollution from the cumulative basicConfig/addHandler calls.
        root = logging.getLogger()
        for handler in root.handlers[:]:
            handler.close()
            root.removeHandler(handler)

    def test_rotating_file_handler_present(self):
        """configure_log must add a RotatingFileHandler to the root logger."""
        configure_log("test_rotate", "DEBUG")
        root_handlers = logging.getLogger().handlers
        rotating_handlers = [h for h in root_handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        self.assertTrue(
            len(rotating_handlers) >= 1,
            "Expected at least one RotatingFileHandler on the root logger",
        )

    def test_rotating_file_handler_settings(self):
        """RotatingFileHandler must use 1 MB max size and 5 backups."""
        configure_log("test_rotate_settings", "DEBUG")
        root_handlers = logging.getLogger().handlers
        rotating_handlers = [h for h in root_handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        self.assertTrue(len(rotating_handlers) >= 1, "No RotatingFileHandler found")
        handler = rotating_handlers[0]
        self.assertEqual(handler.maxBytes, 1_000_000, "maxBytes should be 1_000_000")
        self.assertEqual(handler.backupCount, 5, "backupCount should be 5")


if __name__ == "__main__":
    unittest.main()
