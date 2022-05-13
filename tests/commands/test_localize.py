import gettext
import unittest
import mock
import tabcmd.execution.localize as loc


class LocaleTests(unittest.TestCase):

    def test_defaults(self):
        lang = loc.set_locale()
        assert lang is not None
        assert isinstance(lang, gettext.NullTranslations)
        assert _ is not None
