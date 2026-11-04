import argparse
from unittest.mock import MagicMock

from tabcmd.commands.datasources_and_workbooks.datasources_and_workbooks_command import DatasourcesAndWorkbooks
from tabcmd.commands.datasources_and_workbooks.export_command import ExportCommand
import tableauserverclient as tsc
import unittest
from unittest import mock

mock_logger = mock.MagicMock()

fake_item = mock.MagicMock()
fake_item.name = "fake-name"
fake_item.id = "fake-id"

getter = MagicMock()
getter.get = MagicMock("get", return_value=([fake_item], 1))
getter.get_by_id = MagicMock("get_by_id", return_value=([fake_item], 1))

mock_args = argparse.Namespace()


class ParameterTests(unittest.TestCase):
    def test_get_view_url_from_names(self):
        wb_name = "WB"
        view_name = "VIEW"
        out_value = DatasourcesAndWorkbooks.get_view_url_from_names(wb_name, view_name)
        assert out_value == "{}/sheets/{}".format(wb_name, view_name)

    def test_apply_filters_from_url_params(self):
        query_params = "?Product=widget"
        expected = [("Product", "widget")]
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, query_params)
        assert request_options.view_filters == expected

    def test_apply_encoded_filters_from_url_params(self):
        query_params = "?Product%20type=Z%C3%BCrich"
        expected = [("Product type", "Zürich")]
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, query_params)
        assert request_options.view_filters == expected

    def test_apply_filter_value_with_equals_in_value(self):
        # A filter value containing '=' should survive parsing intact.
        # Old behavior: value.split("=") truncated at the second '=',
        # so "Notes=x=y" incorrectly became name="Notes", value="x".
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_filter_value(mock_logger, request_options, "Notes=x=y")
        assert request_options.view_filters == [("Notes", "x=y")]

    def test_apply_filter_value_with_multiple_equals_in_value(self):
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_filter_value(mock_logger, request_options, "Config=k1=v1=extra")
        assert request_options.view_filters == [("Config", "k1=v1=extra")]

    def test_apply_filter_value_with_trailing_equals(self):
        # Empty string after the '=' should produce an empty-string value.
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_filter_value(mock_logger, request_options, "Name=")
        assert request_options.view_filters == [("Name", "")]

    def test_apply_filter_value_unparseable_strict_exits(self):
        # Default strict=True: a clause missing '=' exits with an error, matching
        # the --filter flag contract.
        request_options = tsc.PDFRequestOptions()
        with self.assertRaises(SystemExit):
            DatasourcesAndWorkbooks.apply_filter_value(mock_logger, request_options, "no_equals_here")

    def test_apply_filter_value_unparseable_non_strict_skips(self):
        # strict=False: unparseable clause is logged and skipped (tabcmd Classic
        # parity for URL-embedded filter fragments like `Field=x&y` where '&' is
        # part of the value and got split into a bogus second fragment).
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_filter_value(mock_logger, request_options, "no_equals_here", strict=False)
        assert request_options.view_filters == []

    def test_apply_values_from_url_params_tolerates_ampersand_in_value(self):
        # Regression: `?Product Name=AT&T 841000 Phone` (Classic drop-in) previously
        # errored on the "T 841000 Phone" fragment produced by the '&' split, and
        # a prior iteration applied "Product Name=AT" as a partial filter (silent
        # wrong-data bug when a dataset had matching "AT" rows). The correct fix
        # is to rejoin fragments so the user's intended value is preserved.
        query = "?Product%20Name=AT&T%20841000%20Phone"
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, query)
        assert request_options.view_filters == [("Product Name", "AT&T 841000 Phone")]

    def test_apply_values_from_url_params_rejoins_multiple_ampersands(self):
        # Multiple '&'s inside a single value should all be rejoined.
        query = "?Company=A%20&%20B%20&%20C"
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, query)
        assert request_options.view_filters == [("Company", "A & B & C")]

    def test_apply_values_from_url_params_options_after_ampersand_not_rejoined(self):
        # An options key (starts with ':') after '&' should NOT be rejoined --
        # that's a legitimate multi-parameter URL.
        query = "?Region=West&:refresh=yes"
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, query)
        assert request_options.view_filters == [("Region", "West")]
        assert request_options.max_age == 0

    def test_apply_values_from_url_params_multiple_filters_not_rejoined(self):
        # Two legitimate filters separated by '&' should stay separate (each
        # fragment has its own '=', so the rejoin heuristic doesn't fire).
        query = "?Region=West&Product=Widget"
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, query)
        assert ("Region", "West") in request_options.view_filters
        assert ("Product", "Widget") in request_options.view_filters

    def test_apply_values_from_url_params_option_after_trailing_ampersand_not_corrupted(self):
        # Regression (Copilot #442): `?:refresh=yes&` splits into [":refresh=yes", ""].
        # The empty trailing fragment must not be rejoined onto the option, and a
        # bare fragment immediately after an option must not be absorbed into it either.
        query = "?:refresh=yes&"
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, query)
        assert request_options.max_age == 0

    def test_apply_values_from_url_params_bare_fragment_after_option_not_absorbed(self):
        # A bare (no '=') fragment immediately following an option key should not
        # be rejoined into the option -- only a preceding *filter* fragment can
        # absorb a stray '&'-split continuation.
        query = "?:refresh=yes&stray"
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, query)
        assert request_options.max_age == 0
        assert request_options.view_filters == []

    def test_apply_options_from_url_params(self):
        query_params = "?:iid=5&:refresh=yes&:size=600,700"
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, query_params)
        assert request_options.max_age == 0

    def test_apply_png_options(self):
        mock_args.width = "800"
        mock_args.height = "76"
        mock_args.resolution = None
        mock_args.language = None
        request_options = tsc.ImageRequestOptions()
        DatasourcesAndWorkbooks.apply_png_options(mock_logger, request_options, mock_args)
        assert request_options.image_resolution == "high"
        assert request_options.viz_width == 800
        assert request_options.viz_height == 76

    def test_apply_png_options_with_language(self):
        mock_args.width = "800"
        mock_args.height = "76"
        mock_args.resolution = None
        mock_args.language = "de"
        request_options = tsc.ImageRequestOptions()
        DatasourcesAndWorkbooks.apply_png_options(mock_logger, request_options, mock_args)
        assert request_options.image_resolution == "high"
        assert request_options.viz_width == 800
        assert request_options.viz_height == 76
        assert request_options.language == "de"

    def test_apply_png_options_with_resolution_high(self):
        mock_args.width = "800"
        mock_args.height = "76"
        mock_args.resolution = "high"
        mock_args.language = None
        request_options = tsc.ImageRequestOptions()
        DatasourcesAndWorkbooks.apply_png_options(mock_logger, request_options, mock_args)
        assert request_options.image_resolution == "high"
        assert request_options.viz_width == 800
        assert request_options.viz_height == 76

    def test_apply_png_options_with_resolution_standard(self):
        mock_args.width = "800"
        mock_args.height = "76"
        mock_args.resolution = "standard"
        mock_args.language = None
        request_options = tsc.ImageRequestOptions()
        DatasourcesAndWorkbooks.apply_png_options(mock_logger, request_options, mock_args)
        assert request_options.image_resolution is None
        assert request_options.viz_width == 800
        assert request_options.viz_height == 76

    def test_apply_png_options_bad_values(self):
        mock_args.height = "seven"
        mock_args.width = "800b"
        request_options = tsc.ImageRequestOptions()
        with self.assertRaises(ValueError):
            DatasourcesAndWorkbooks.apply_png_options(mock_logger, request_options, mock_args)

    def test_apply_pdf_options(self):
        expected_page = tsc.PDFRequestOptions.PageType.Folio.__str__()
        expected_layout = tsc.PDFRequestOptions.Orientation.Portrait.__str__()
        expected_height = 800
        expected_width = 600
        mock_args.pagelayout = expected_layout
        mock_args.pagesize = expected_page
        mock_args.height = expected_height
        mock_args.width = expected_width
        mock_args.language = None
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_pdf_options(mock_logger, request_options, mock_args)
        assert request_options.page_type == expected_page
        assert request_options.orientation == expected_layout
        assert request_options.viz_width == expected_width
        assert request_options.viz_height == expected_height

    def test_apply_pdf_options_with_language(self):
        language = "de"
        expected_page = tsc.PDFRequestOptions.PageType.Folio.__str__()
        expected_layout = tsc.PDFRequestOptions.Orientation.Portrait.__str__()
        mock_args.pagelayout = expected_layout
        mock_args.pagesize = expected_page
        mock_args.language = language
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_pdf_options(mock_logger, request_options, mock_args)
        assert request_options.page_type == expected_page
        assert request_options.orientation == expected_layout
        assert request_options.language == language

    def test_apply_options_in_url_with_size(self):
        request_options = tsc.ImageRequestOptions()
        DatasourcesAndWorkbooks.apply_options_in_url(mock_logger, request_options, ":size=1920,1080")
        self.assertEqual(request_options.viz_width, 1920)
        self.assertEqual(request_options.viz_height, 1080)

    def test_apply_options_in_url_with_size_via_url_params(self):
        request_options = tsc.ImageRequestOptions()
        DatasourcesAndWorkbooks.apply_values_from_url_params(mock_logger, request_options, "?:size=1920,1080")
        self.assertEqual(request_options.viz_width, 1920)
        self.assertEqual(request_options.viz_height, 1080)

    def test_apply_options_in_url_with_refresh(self):
        request_options = tsc.ImageRequestOptions()
        value = ":refresh=yes"

        DatasourcesAndWorkbooks.apply_options_in_url(mock_logger, request_options, value)
        self.assertEqual(request_options.max_age, 0)

    def test_apply_options_in_url_with_invalid_size(self):
        request_options = tsc.ImageRequestOptions()
        value = ":size=invalid"

        DatasourcesAndWorkbooks.apply_options_in_url(mock_logger, request_options, value)
        self.assertEqual(request_options.viz_height, None)
        self.assertEqual(request_options.viz_width, None)

    def test_apply_options_in_url_invalid_first_dimension_leaves_both_unset(self):
        request_options = tsc.ImageRequestOptions()
        DatasourcesAndWorkbooks.apply_options_in_url(mock_logger, request_options, ":size=notanumber,600")
        self.assertIsNone(request_options.viz_width)
        self.assertIsNone(request_options.viz_height)

    def test_apply_options_in_url_invalid_second_dimension_leaves_both_unset(self):
        request_options = tsc.ImageRequestOptions()
        DatasourcesAndWorkbooks.apply_options_in_url(mock_logger, request_options, ":size=1920,notanumber")
        self.assertIsNone(request_options.viz_width)
        self.assertIsNone(request_options.viz_height)

    def test_apply_options_in_url_with_unrecognized_parameter(self):
        request_options = tsc.ImageRequestOptions()
        default_max_age = request_options.max_age
        value = ":unknown=param"

        DatasourcesAndWorkbooks.apply_options_in_url(mock_logger, request_options, value)
        self.assertEqual(request_options.viz_height, None)
        self.assertEqual(request_options.viz_width, None)
        self.assertEqual(request_options.max_age, default_max_age)

    def test_apply_csv_options(self):
        mock_args.language = None
        request_options = tsc.CSVRequestOptions()
        DatasourcesAndWorkbooks.apply_csv_options(mock_logger, request_options, mock_args)
        assert request_options.language == None

    def test_apply_csv_options_with_language(self):
        mock_args.language = "de"
        mock_args.country = None
        request_options = tsc.CSVRequestOptions()
        DatasourcesAndWorkbooks.apply_csv_options(mock_logger, request_options, mock_args)
        assert request_options.language == "de"

    def test_apply_csv_options_with_language_and_country(self):
        # tabcmd Classic combined --language + --country into a locale (issue #109).
        local_args = argparse.Namespace(language="en", country="GB")
        request_options = tsc.CSVRequestOptions()
        DatasourcesAndWorkbooks.apply_csv_options(mock_logger, request_options, local_args)
        assert request_options.language == "en-GB"

    def test_apply_png_options_with_language_and_country(self):
        local_args = argparse.Namespace(language="fr", country="CA", height="600", width="800", resolution=None)
        request_options = tsc.ImageRequestOptions()
        DatasourcesAndWorkbooks.apply_png_options(mock_logger, request_options, local_args)
        assert request_options.language == "fr-CA"

    def test_apply_pdf_options_with_language_and_country(self):
        local_args = argparse.Namespace(
            language="pt",
            country="BR",
            height=800,
            width=600,
            pagelayout=tsc.PDFRequestOptions.Orientation.Portrait.__str__(),
            pagesize=tsc.PDFRequestOptions.PageType.Folio.__str__(),
        )
        request_options = tsc.PDFRequestOptions()
        DatasourcesAndWorkbooks.apply_pdf_options(mock_logger, request_options, local_args)
        assert request_options.language == "pt-BR"

    def test_resolve_locale_country_without_language_is_dropped(self):
        # --country alone is not a valid locale; drop it and don't send to server.
        local_args = argparse.Namespace(language=None, country="US")
        assert DatasourcesAndWorkbooks._resolve_locale(local_args) is None

    def test_resolve_locale_country_without_language_warns(self):
        # The user's --country was silently dropped in prior revisions; make sure
        # they get a warning. Depending on whether the gettext catalog is loaded
        # `_()` returns either the raw key or the English message; the user-supplied
        # country value is formatted into either, so assert on that.
        local_args = argparse.Namespace(language=None, country="US")
        warn_logger = mock.MagicMock()
        assert DatasourcesAndWorkbooks._resolve_locale(local_args, warn_logger) is None
        warn_logger.warning.assert_called_once()
        assert "US" in warn_logger.warning.call_args[0][0]

    def test_resolve_locale_language_only(self):
        local_args = argparse.Namespace(language="ja", country=None)
        assert DatasourcesAndWorkbooks._resolve_locale(local_args) == "ja"

    def test_resolve_locale_language_only_does_not_warn(self):
        local_args = argparse.Namespace(language="ja", country=None)
        warn_logger = mock.MagicMock()
        DatasourcesAndWorkbooks._resolve_locale(local_args, warn_logger)
        warn_logger.warning.assert_not_called()

    def test_apply_filters_from_args_none(self):
        args = argparse.Namespace(filter=None)
        request_options = tsc.PDFRequestOptions()
        ExportCommand.apply_filters_from_args(request_options, args, mock_logger)
        assert request_options.view_filters == []

    def test_apply_filters_from_args_single(self):
        args = argparse.Namespace(filter=["Region=West"])
        request_options = tsc.PDFRequestOptions()
        ExportCommand.apply_filters_from_args(request_options, args, mock_logger)
        assert request_options.view_filters == [("Region", "West")]

    def test_apply_filters_from_args_repeated(self):
        # repeated --filter flags each carry one pair, so '&' in a value is safe.
        args = argparse.Namespace(filter=["Region=West", "Product=AT&T"])
        request_options = tsc.PDFRequestOptions()
        ExportCommand.apply_filters_from_args(request_options, args, mock_logger)
        assert request_options.view_filters == [("Region", "West"), ("Product", "AT&T")]

    def test_apply_filters_from_args_backcompat_ampersand_join(self):
        # Old-style single flag joining pairs with '&' still parses.
        args = argparse.Namespace(filter=["Region=West&Product=Widget"])
        request_options = tsc.PDFRequestOptions()
        ExportCommand.apply_filters_from_args(request_options, args, mock_logger)
        assert request_options.view_filters == [("Region", "West"), ("Product", "Widget")]

    def test_apply_filters_from_args_single_with_literal_ampersand(self):
        # Regression: a single --filter whose value contains a literal '&' but is not
        # a '&'-joined COLUMN=VALUE pair list must not be split into bogus segments
        # (which previously could raise IndexError downstream in apply_filter_value).
        args = argparse.Namespace(filter=["Company=AT&T"])
        request_options = tsc.PDFRequestOptions()
        ExportCommand.apply_filters_from_args(request_options, args, mock_logger)
        assert request_options.view_filters == [("Company", "AT&T")]

    def test_apply_filters_from_args_preserves_equals_in_value(self):
        # Regression: values containing '=' (e.g. "Notes=x=y") must not be truncated.
        args = argparse.Namespace(filter=["Notes=x=y"])
        request_options = tsc.PDFRequestOptions()
        ExportCommand.apply_filters_from_args(request_options, args, mock_logger)
        assert request_options.view_filters == [("Notes", "x=y")]


@mock.patch("tableauserverclient.Server")
class MockedServerTests(unittest.TestCase):
    def test_mock_getter(self, mock_server):
        mock_server.fakes = getter
        mock_server.fakes.get()
        getter.get.assert_called()

    def test_get_ds_by_content_url(self, mock_server):
        mock_server.datasources = getter
        content_url = "blah"
        DatasourcesAndWorkbooks.get_ds_by_content_url(mock_logger, mock_server, content_url)
        getter.get.assert_called()
        # should also assert the filter on content url

    def test_get_wb_by_content_url(self, mock_server):
        mock_server.workbooks = getter
        content_url = "blah"
        DatasourcesAndWorkbooks.get_wb_by_content_url(mock_logger, mock_server, content_url)
        getter.get.assert_called()
        # should also assert the filter on content url

    def test_get_view_by_content_url(self, mock_server):
        mock_server.views = getter
        content_url = "blah"
        DatasourcesAndWorkbooks.get_view_by_content_url(mock_logger, mock_server, content_url)
        getter.get.assert_called()
        # should also assert the filter on content url

    def test_get_custom_view_by_id(self, mock_server):
        mock_server.custom_views = getter
        custom_view_id = "cv-id"
        DatasourcesAndWorkbooks.get_custom_view_by_id(mock_logger, mock_server, custom_view_id)
        getter.get_by_id.assert_called()


def _filters_from_args(value):
    request_options = tsc.PDFRequestOptions()
    ExportCommand.apply_filters_from_args(request_options, argparse.Namespace(filter=[value]), mock.MagicMock())
    return request_options.view_filters


def _filters_from_url(url, logger=None):
    request_options = tsc.PDFRequestOptions()
    DatasourcesAndWorkbooks.apply_values_from_url_params(logger or mock.MagicMock(), request_options, url)
    return request_options.view_filters


class FilterFlagTests(unittest.TestCase):
    """The --filter flag path, through apply_filters_from_args."""

    def test_equals_in_value_survives_the_flag_path(self):
        assert _filters_from_args("Notes=x=y") == [("Notes", "x=y")]

    def test_ampersand_separates_filters(self):
        assert _filters_from_args("Region=West&Product=Widget") == [("Region", "West"), ("Product", "Widget")]

    def test_trailing_ampersand_is_ignored(self):
        assert _filters_from_args("Region=West&") == [("Region", "West")]

    def test_ampersand_inside_value_is_literal(self):
        # Matches test_apply_filters_from_args_single_with_literal_ampersand: "AT&T" has no
        # clean COLUMN=VALUE split, so the single --filter is passed through whole.
        assert _filters_from_args("Product=AT&T") == [("Product", "AT&T")]

    def test_empty_name_exits(self):
        with self.assertRaises(SystemExit):
            DatasourcesAndWorkbooks.apply_filter_value(mock.MagicMock(), tsc.PDFRequestOptions(), "=x")


class UrlFilterTests(unittest.TestCase):
    """Filters embedded in the view URL, through apply_values_from_url_params."""

    def test_parameters_prefix_is_stripped_before_rejoin(self):
        assert _filters_from_url("?Parameters.Company=A%20&%20B") == [("Company", "A & B")]

    def test_rejoin_logs_a_warning(self):
        logger = mock.MagicMock()
        _filters_from_url("?Product=AT&T", logger)
        logger.warning.assert_called_once()

    def test_bare_url_filter_is_skipped(self):
        assert _filters_from_url("?Region") == []

    def test_empty_name_in_url_is_skipped(self):
        assert _filters_from_url("?=x") == []

    def test_value_with_ampersand_and_equals_is_split(self):
        # Known limitation: "AT&T x=y Combo" is indistinguishable from two filters.
        assert _filters_from_url("?Product%20Name=AT&T%20x=y%20Combo") == [
            ("Product Name", "AT"),
            ("T x", "y Combo"),
        ]
