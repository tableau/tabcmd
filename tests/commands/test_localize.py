import gettext
import unittest
from tabcmd.execution.localize import set_client_locale


class LocaleTests(unittest.TestCase):
    def test_defaults(self):
        translations = set_client_locale()
        assert translations is not None
        # False: bound method != function ?
        # assert translations == gettext.NullTranslations.gettext

    def test_en_smoke_launching(self):
        # 27 incidents of this string
        translations = set_client_locale()
        assert translations is not None

        assert _("tabcmd.launching") == "======================= Launching command ======================="

    def test_en_smoke_publish_errors(self):
        # 8 incidents of this string
        translations = set_client_locale()
        assert translations is not None

        assert _("publish.errors.unexpected_server_response") == "Unexpected response from the server: {0}"

    def test_en_smoke_output_succeeded(self):
        # 8 incidents of this string
        translations = set_client_locale()
        assert translations is not None

        assert _("common.output.succeeded") == "Succeeded"

    def test_en_smoke_percent_complete(self):
        # 5 incidents of this string
        translations = set_client_locale()
        assert translations is not None

        assert _("session.monitorjob.percent_complete") == "{0}% complete"

    def test_en_smoke_line_processed(self):
        # 5 incidents of this string
        translations = set_client_locale()
        assert translations is not None

        assert _("importcsvsummary.line.processed") == "Lines processed: {0}"
