import io
import logging
import logging.handlers
import sys
import unittest
from unittest import mock

from tabcmd.execution.logger_config import configure_log


def _clear_handlers():
    root = logging.getLogger()
    for handler in root.handlers[:]:
        handler.close()
        root.removeHandler(handler)
    for name in list(logging.Logger.manager.loggerDict):
        if name.startswith("test_"):
            logging.getLogger(name).handlers.clear()


class LoggerConfigTests(unittest.TestCase):
    def setUp(self):
        _clear_handlers()

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

    def test_no_duplicate_file_handlers_on_repeated_calls(self):
        configure_log("test_dup", "DEBUG")
        configure_log("test_dup", "DEBUG")
        root_handlers = logging.getLogger().handlers
        rotating = [h for h in root_handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        self.assertEqual(len(rotating), 1, "Repeated configure_log calls must not add duplicate file handlers")

    def test_no_duplicate_console_handlers_on_repeated_calls(self):
        fake_out, fake_err = io.StringIO(), io.StringIO()
        with mock.patch("sys.stdout", fake_out), mock.patch("sys.stderr", fake_err):
            configure_log("test_dup_console", "DEBUG")
            configure_log("test_dup_console", "DEBUG")
        named = logging.getLogger("test_dup_console")
        stream_handlers = [
            h for h in named.handlers if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        ]
        self.assertEqual(len(stream_handlers), 2, "Repeated calls must not add more than 2 console handlers")

    def test_root_logger_level_set(self):
        configure_log("test_level", "WARNING")
        self.assertEqual(logging.getLogger().level, logging.WARNING)


class StdoutStderrSplitTests(unittest.TestCase):
    """INFO goes to stdout; WARNING+ goes to stderr."""

    def setUp(self):
        _clear_handlers()

    def _make_logger(self, name):
        fake_out, fake_err = io.StringIO(), io.StringIO()
        with mock.patch("sys.stdout", fake_out), mock.patch("sys.stderr", fake_err):
            logger = configure_log(name, "DEBUG")
        logger.propagate = False
        return logger, fake_out, fake_err

    def test_two_stream_handlers_attached(self):
        logger, _, _ = self._make_logger("test_split_two_handlers")
        stream_handlers = [
            h
            for h in logger.handlers
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        ]
        self.assertEqual(len(stream_handlers), 2)

    def test_stdout_and_stderr_handlers_bound_to_correct_streams(self):
        fake_out, fake_err = io.StringIO(), io.StringIO()
        with mock.patch("sys.stdout", fake_out), mock.patch("sys.stderr", fake_err):
            logger = configure_log("test_split_streams", "DEBUG")
        stream_handlers = [
            h
            for h in logger.handlers
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        ]
        streams = {h.stream for h in stream_handlers}
        self.assertIn(fake_out, streams)
        self.assertIn(fake_err, streams)

    def test_info_goes_to_stdout_not_stderr(self):
        logger, fake_out, fake_err = self._make_logger("test_split_info")
        logger.info("hello stdout")
        self.assertIn("hello stdout", fake_out.getvalue())
        self.assertNotIn("hello stdout", fake_err.getvalue())

    def test_warning_goes_to_stderr_not_stdout(self):
        logger, fake_out, fake_err = self._make_logger("test_split_warning")
        logger.warning("a warning")
        self.assertNotIn("a warning", fake_out.getvalue())
        self.assertIn("a warning", fake_err.getvalue())

    def test_error_goes_to_stderr_not_stdout(self):
        logger, fake_out, fake_err = self._make_logger("test_split_error")
        logger.error("an error")
        self.assertNotIn("an error", fake_out.getvalue())
        self.assertIn("an error", fake_err.getvalue())

    def test_no_double_print_from_sibling_loggers(self):
        """Two distinct leaf loggers sharing the same streams must not double-print."""
        fake_out, fake_err = io.StringIO(), io.StringIO()
        with mock.patch("sys.stdout", fake_out), mock.patch("sys.stderr", fake_err):
            logger_a = configure_log("test_split_sibling_a", "DEBUG")
            configure_log("test_split_sibling_b", "DEBUG")
        logger_a.propagate = False
        logger_a.info("msg from a")
        self.assertEqual(fake_out.getvalue().count("msg from a"), 1, "Message should appear exactly once")


if __name__ == "__main__":
    unittest.main()
