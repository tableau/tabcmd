import gettext
import locale
import sys
import unittest
from tabcmd.execution.localize import set_client_locale, _get_default_locale


class LocaleTests(unittest.TestCase):
    def test_defaults(self):
        translations = set_client_locale()
        assert translations is not None
        # False: bound method != function ?
        # assert translations == gettext.NullTranslations.gettext

    def test_en_smoke_publish_errors(self):
        # 8 incidents of this string
        translations = set_client_locale()
        assert translations is not None

        assert translations("publish.errors.unexpected_server_response") == "Unexpected response from the server: {0}"

    def test_en_smoke_output_succeeded(self):
        # 8 incidents of this string
        translations = set_client_locale()
        assert translations is not None

        assert translations("common.output.succeeded") == "Succeeded"

    def test_en_smoke_percent_complete(self):
        # 5 incidents of this string
        translations = set_client_locale()
        assert translations is not None

        assert translations("session.monitorjob.percent_complete") == "{0}% complete"

    def test_en_smoke_line_processed(self):
        # 5 incidents of this string
        translations = set_client_locale()
        assert translations is not None

        assert translations("importcsvsummary.line.processed") == "Lines processed: {0}"

    #  https://docs.python.org/3/library/locale.html
    #  c:\dev\tabcmd\tabcmd\execution\localize.py:85: DeprecationWarning:
    # 'locale.getdefaultlocale' is deprecated and slated for removal in Python 3.15. Use setlocale(), getencoding() and getlocale() instead
    def test_get_default_locale(self):
        # Our method in localize.py that needs to change. An eventual unit test should call this method.
        # loc = _get_default_locale()  # doesn't return anything: need to mock _validate_lang

        # This bug on pytest explains why the proposed replacements aren't directly equivalent.
        # Some people online have solved this with manual string mangling. I like the pytest decision
        # to wait until we hit 3.15 and hope someone has implemented a better option by then.
        # current call that is deprecated -->loc = locale.getdefaultlocale()  # returns ('en_US', 'cp1252')
        # sys.getdefaultencoding()  # returns utf-8
        # locale.getlocale()  # returns ('English_United States', '1252')
        new_locale = locale.setlocale(locale.LC_CTYPE, None)  # returns English_United States.125
        # assert loc == new_locale
