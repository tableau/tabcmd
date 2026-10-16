import unittest

from tabcmd.commands.site.edit_site_command import EditSiteCommand
from .common_setup import *

commandname = "editsites"


class EditSiteParserTest(ParserTest):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, EditSiteCommand)

    def test_edit_site_parser_optional_args_present(self):
        mock_args = [
            commandname,
            "site-to-edit",
            "--site-name",
            "new-site-name",
            "--user-quota",
            "12",
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.site_name == "site-to-edit", args
        assert args.new_site_name == "new-site-name", args
        assert args.user_quota == 12, args

    def test_edit_site_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    """
    bug: this should probably exit unhappy?
    def test_edit_site_parser_missing_all_args(self):
        mock_args = [commandname, 'site-to-edit']
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
    """

    def test_edit_site_parser_storage_quota_integer(self):
        mock_args = [commandname, "site-to-edit", "--storage-quota", "12"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.site_name == "site-to-edit", args
        assert args.storage_quota == 12, args

    def test_edit_site_parser_optional_arguments_archive(self):
        mock_args = [
            commandname,
            "site-to-edit",
            "--status",
            "ACTIVE",
            "--site-id",
            "1234",
            "--run-now-enabled",
            "true",
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.site_id == "1234", args
        assert args.status == "ACTIVE", args
        assert args.run_now_enabled == "true", args

    # -------- New flags added for issue #437 --------

    def test_edit_site_parser_guest_access_enabled_true(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--guest-access-enabled", "true"])
        assert args.guest_access_enabled == "true", args

    def test_edit_site_parser_guest_access_enabled_short_flag(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "-g", "false"])
        assert args.guest_access_enabled == "false", args

    def test_edit_site_parser_guest_access_enabled_rejects_invalid(self):
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args([commandname, "site-to-edit", "--guest-access-enabled", "yes"])

    def test_edit_site_parser_cache_warmup_enabled(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--cache-warmup"])
        assert args.cache_warmup_enabled is True, args

    def test_edit_site_parser_cache_warmup_disabled(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--no-cache-warmup"])
        assert args.cache_warmup_enabled is False, args

    def test_edit_site_parser_cache_warmup_default_is_none(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit"])
        assert args.cache_warmup_enabled is None, args

    def test_edit_site_parser_cache_warmup_mutually_exclusive(self):
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args([commandname, "site-to-edit", "--cache-warmup", "--no-cache-warmup"])

    def test_edit_site_parser_subscription_email(self):
        args = self.parser_under_test.parse_args(
            [commandname, "site-to-edit", "--subscription-email", "alerts@example.com"]
        )
        assert args.subscription_email == "alerts@example.com", args

    def test_edit_site_parser_subscription_email_short_flag(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "-e", "hi@example.com"])
        assert args.subscription_email == "hi@example.com", args

    def test_edit_site_parser_subscription_footer(self):
        args = self.parser_under_test.parse_args(
            [commandname, "site-to-edit", "--subscription-footer", "Contact IT for help"]
        )
        assert args.subscription_footer == "Contact IT for help", args

    def test_edit_site_parser_subscription_footer_short_flag(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "-f", "Contact IT"])
        assert args.subscription_footer == "Contact IT", args

    def test_edit_site_parser_web_extraction_enabled(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--web-extraction-enabled", "true"])
        assert args.web_extraction_enabled == "true", args

    def test_edit_site_parser_web_extraction_enabled_rejects_invalid(self):
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args([commandname, "site-to-edit", "--web-extraction-enabled", "yes"])

    def test_edit_site_parser_allow_subscriptions(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--allow-subscriptions"])
        assert args.allow_subscriptions is True, args

    def test_edit_site_parser_no_allow_subscriptions(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--no-allow-subscriptions"])
        assert args.allow_subscriptions is False, args

    def test_edit_site_parser_allow_subscriptions_default_is_none(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit"])
        assert args.allow_subscriptions is None, args

    def test_edit_site_parser_allow_subscriptions_mutually_exclusive(self):
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(
                [
                    commandname,
                    "site-to-edit",
                    "--allow-subscriptions",
                    "--no-allow-subscriptions",
                ]
            )

    def test_edit_site_parser_allow_web_authoring(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--allow-web-authoring"])
        assert args.allow_web_authoring is True, args

    def test_edit_site_parser_no_allow_web_authoring(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--no-allow-web-authoring"])
        assert args.allow_web_authoring is False, args

    def test_edit_site_parser_allow_web_authoring_mutually_exclusive(self):
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(
                [
                    commandname,
                    "site-to-edit",
                    "--allow-web-authoring",
                    "--no-allow-web-authoring",
                ]
            )

    def test_edit_site_parser_allow_mobile_snapshots(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--allow-mobile-snapshots"])
        assert args.allow_mobile_snapshots is True, args

    def test_edit_site_parser_no_allow_mobile_snapshots(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--no-allow-mobile-snapshots"])
        assert args.allow_mobile_snapshots is False, args

    def test_edit_site_parser_allow_mobile_snapshots_mutually_exclusive(self):
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(
                [
                    commandname,
                    "site-to-edit",
                    "--allow-mobile-snapshots",
                    "--no-allow-mobile-snapshots",
                ]
            )

    def test_edit_site_parser_time_zone(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--time-zone", "America/Los_Angeles"])
        assert args.time_zone == "America/Los_Angeles", args

    def test_edit_site_parser_use_default_time_zone(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--use-default-time-zone"])
        assert args.use_default_time_zone is True, args

    def test_edit_site_parser_time_zone_mutually_exclusive(self):
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(
                [
                    commandname,
                    "site-to-edit",
                    "--time-zone",
                    "UTC",
                    "--use-default-time-zone",
                ]
            )

    # -------- default=None coverage for the remaining new flags --------
    # An unpassed flag must leave the SiteItem attribute untouched. If any of
    # these defaulted to False, every editsite call would flip the setting off.

    def test_edit_site_parser_guest_access_enabled_default_is_none(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit"])
        assert args.guest_access_enabled is None, args

    def test_edit_site_parser_web_extraction_enabled_default_is_none(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit"])
        assert args.web_extraction_enabled is None, args

    def test_edit_site_parser_allow_web_authoring_default_is_none(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit"])
        assert args.allow_web_authoring is None, args

    def test_edit_site_parser_allow_mobile_snapshots_default_is_none(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit"])
        assert args.allow_mobile_snapshots is None, args

    def test_edit_site_parser_subscription_email_default_is_none(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit"])
        assert args.subscription_email is None, args

    def test_edit_site_parser_subscription_footer_default_is_none(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit"])
        assert args.subscription_footer is None, args

    def test_edit_site_parser_time_zone_default_is_none(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit"])
        assert args.time_zone is None, args

    # -------- Explicit "false" acceptance on string-value flags --------
    # The short-flag test for --guest-access-enabled uses "false" but
    # --web-extraction-enabled only had a "true" test. Cover both.

    def test_edit_site_parser_guest_access_enabled_long_flag_false(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--guest-access-enabled", "false"])
        assert args.guest_access_enabled == "false", args

    def test_edit_site_parser_web_extraction_enabled_false(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--web-extraction-enabled", "false"])
        assert args.web_extraction_enabled == "false", args

    # -------- Empty-string-as-disable on email/footer --------
    # `bool('')` is False, so passing an empty string is the convention for
    # clearing the value and disabling the feature. Lock the parsing side in
    # here; the paired _enabled flip happens in run_command.

    def test_edit_site_parser_subscription_email_accepts_empty_string(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--subscription-email", ""])
        assert args.subscription_email == "", args

    def test_edit_site_parser_subscription_footer_accepts_empty_string(self):
        args = self.parser_under_test.parse_args([commandname, "site-to-edit", "--subscription-footer", ""])
        assert args.subscription_footer == "", args
