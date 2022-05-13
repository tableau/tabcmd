import gettext
import unittest
from tabcmd.execution.localize import set_client_locale


class LocaleTests(unittest.TestCase):
    def test_defaults(self):
        _ = set_client_locale()
        assert _ is not None
        # False: bound method != function ?
        # assert _ == gettext.NullTranslations.gettext
