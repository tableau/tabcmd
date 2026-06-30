import logging
import logging.handlers
import unittest

from tabcmd.execution.logger_config import configure_log


class LoggerConfigTests(unittest.TestCase):
    def setUp(self):
        root = logging.getLogger()
        for handler in root.handlers[:]:
            handler.close()
            root.removeHandler(handler)

    def test_rotating_file_handler_present(self):
        configure_log("test_rotate", "DEBUG")
        root_handlers = logging.getLogger().handlers
        rotating = [h for h in root_handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        self.assertEqual(len(rotating), 1, "Expected exactly one RotatingFileHandler on the root logger")

    def test_rotating_file_handler_settings(self):
        configure_log("test_rotate_settings", "DEBUG")
        root_handlers = logging.getLogger().handlers
        rotating = [h for h in root_handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        self.assertEqual(len(rotating), 1, "Expected exactly one RotatingFileHandler on the root logger")
        handler = rotating[0]
        self.assertEqual(handler.maxBytes, 1_000_000)
        self.assertEqual(handler.backupCount, 5)

    def test_no_duplicate_handlers_on_repeated_calls(self):
        configure_log("test_dup", "DEBUG")
        configure_log("test_dup", "DEBUG")
        root_handlers = logging.getLogger().handlers
        rotating = [h for h in root_handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        self.assertEqual(len(rotating), 1, "Repeated configure_log calls must not add duplicate handlers")

    def test_root_logger_level_set(self):
        configure_log("test_level", "WARNING")
        self.assertEqual(logging.getLogger().level, logging.WARNING)


if __name__ == "__main__":
    unittest.main()
