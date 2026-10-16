import logging
import unittest

from tabcmd.execution import localize


class LocalizeFallbackTests(unittest.TestCase):
    def test_untranslated_key_falls_back_to_english(self):
        key = "session.errors.password_file_not_found"
        translate = localize._load_language("de", "tabcmd", logging.getLogger("test"))
        text = translate(key)
        assert text != key, text
        assert "{0}" in text, text
