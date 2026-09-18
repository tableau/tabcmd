import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


def _str_to_bool(value):
    """Coerce a 'true'/'false' string (from argparse choices) to a real bool.

    TSC SiteItem boolean setters are guarded by @property_is_boolean and reject
    strings, so we must convert before assignment.
    """
    if value is None:
        return None
    return str(value).lower() == "true"


class EditSiteCommand(Server):
    """
    Command to change the name of a site or its web folder name. Users can also use this command to allow or deny
    site administrators the ability to add and remove users, or prevent users from running certain tasks manually.
    """

    name: str = "editsite"
    description: str = _("editsite.short_description")

    @staticmethod
    def define_args(edit_site_parser):
        args_group = edit_site_parser.add_argument_group(title=EditSiteCommand.name)
        args_group.add_argument("site_name", metavar="site-name", help="editsite.options.site-name")
        args_group.add_argument("--site-name", default=None, dest="new_site_name", help=_("editsite.options.site-name"))
        set_common_site_args(args_group)
        set_site_status_arg(args_group)
        set_edit_site_only_args(args_group)

    @classmethod
    def run_command(cls, args):
        logger = log(cls.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)

        site_item = Server.get_site_for_command_or_throw(logger, server, args.site_name)
        if args.url:
            site_item.content_url = args.url
        if args.user_quota:
            site_item.user_quota = args.user_quota
        if args.storage_quota:
            site_item.storage_quota = args.storage_quota
        if args.status:
            site_item.state = args.status

        # New flags for W-tabcmd-437. Every attribute is only touched when the
        # corresponding argparse dest is not None, so an unpassed flag leaves
        # the server-side setting unchanged.
        if getattr(args, "guest_access_enabled", None) is not None:
            site_item.guest_access_enabled = _str_to_bool(args.guest_access_enabled)

        if getattr(args, "cache_warmup_enabled", None) is not None:
            site_item.cache_warmup_enabled = args.cache_warmup_enabled

        if getattr(args, "subscription_email", None) is not None:
            # Matches Classic: set the value AND toggle the *_enabled flag.
            # An empty string clears the value and disables the feature.
            # NOTE: TSC RequestFactory currently lowercases this value (bug to
            # file upstream); user@Domain.com will be sent as user@domain.com.
            site_item.custom_subscription_email = args.subscription_email
            site_item.custom_subscription_email_enabled = bool(args.subscription_email)

        if getattr(args, "subscription_footer", None) is not None:
            # Same two-attribute wiring as subscription_email. TSC also
            # lowercases this string; tracked as an upstream TSC bug.
            site_item.custom_subscription_footer = args.subscription_footer
            site_item.custom_subscription_footer_enabled = bool(args.subscription_footer)

        if getattr(args, "web_extraction_enabled", None) is not None:
            site_item.web_extraction_enabled = _str_to_bool(args.web_extraction_enabled)

        if getattr(args, "allow_subscriptions", None) is not None:
            # Inverted: REST API exposes this as disableSubscriptions.
            site_item.disable_subscriptions = not args.allow_subscriptions

        if getattr(args, "allow_web_authoring", None) is not None:
            site_item.authoring_enabled = args.allow_web_authoring

        if getattr(args, "allow_mobile_snapshots", None) is not None:
            site_item.sheet_image_enabled = args.allow_mobile_snapshots

        if getattr(args, "use_default_time_zone", None):
            # Only set use_default_time_zone; do NOT set time_zone -- argparse
            # already enforces mutual exclusion between the two flags.
            site_item.use_default_time_zone = True
        elif getattr(args, "time_zone", None) is not None:
            site_item.time_zone = args.time_zone

        try:
            logger.info(_("editsite.status").format(site_item.name))
            server.sites.update(site_item)
            logger.info(_("common.output.succeeded"))

        except Exception as e:
            Errors.exit_with_error(logger, exception=e)
