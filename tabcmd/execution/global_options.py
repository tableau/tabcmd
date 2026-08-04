import argparse

from .localize import _

"""
- all arguments in here are optional, must be --argument
- all methods in here should return a parser for nice fluent chaining

Method naming conventions
- I have named methods in here aaaa_arg if it returns a value we want, aaa_option if it's a flag
- if not otherwise specified, the value passed in with the arg will be saved as args.argname
- options that just need to turn on or off a flag should be set with action=store_True/False
- for optional arguments, try to use argname: --site-name gets saved as variablename: site_name

All these optional arguments could be used with any command. 
Ideally *all* optional args would be in here, so they can be kept updated together and simply listed on the relevant parser.

Positional arguments will generally be set directly in each parser
Naming note: cannot have hyphens in positional args 
SO define them as add_argument([name for args attribute], metavar=[name to show in help])
e.g add_argument(site, metavar='site-name')
FOR site-name, project-name, workbook-name, datasource-name, group-name, schedule-name, token-name
-> in args: site, project, workbook, ....
BUT filename, username -> filename, username in command/parser

"""

# argparse does case-sensitive comparisons of string inputs by default
# I want the user to be able to enter e.g. "viewer" and have it accepted as "Viewer"
# https://stackoverflow.com/questions/56838004/
# case-insensitive-argparse-choices-without-losing-case-information-in-choices-lis
def case_insensitive_string_type(choices):
    def find_choice(choice):
        for key, item in enumerate([choice.lower() for choice in choices]):
            if choice.lower() == item:
                return choices[key]
        else:
            return choice

    return find_choice


def set_parent_project_arg(parser):
    parser.add_argument("--parent-project-path", default=None, help=_("tabcmd.options.parent_project"))
    return parser


# add/remove-user
# parser.users command has a bunch of deprecated options. Just ditch them?
# --admin-type, --[no-]publisher, --[no-]complete (which was ssuuuuubtly different from add-users)


def set_users_file_arg(parser):
    parser.add_argument(
        "--users",
        required=True,
        type=argparse.FileType("r", encoding="utf-8-sig"),
        help=_("tabcmd.options.users_file"),
    )
    return parser


def set_users_file_positional(parser):
    parser.add_argument(
        "filename",
        metavar="filename.csv",
        type=argparse.FileType("r", encoding="utf-8-sig"),
        help=_("tabcmd.options.users_file"),
    )
    return parser


def set_no_wait_option(parser):
    parser.add_argument("--no-wait", action="store_true", help=_("common.options.nowait"))
    return parser


def set_silent_option(parser):
    parser.add_argument("--silent-progress", action="store_true", help=_("common.options.silent-progress"))
    return parser


def set_completeness_options(parser):
    completeness_group = parser.add_mutually_exclusive_group()
    completeness_group.add_argument(
        "--complete",
        dest="require_all_valid",
        action="store_true",
        help=_("tabcmd.options.complete"),
    )
    completeness_group.add_argument(
        "--no-complete",
        dest="require_all_valid",
        action="store_false",
        help=_("tabcmd.options.no_complete"),
    )
    completeness_group.set_defaults(require_all_valid=True)
    return parser


# used in create/delete extract
def set_embedded_datasources_options(parser):
    # one of these is required IFF we are using a workbook instead of datasource
    embedded_group = parser.add_mutually_exclusive_group()
    embedded_group.add_argument(  # nargs?
        "--embedded-datasources",
        help=_("createextracts.options.embedded-datasources"),
    )
    embedded_group.add_argument("--include-all", action="store_true", help=_("createextracts.options.include-all"))
    return parser


# used in create extract. listed in delete-extract but makes no sense there
def set_encryption_option(parser):
    parser.add_argument(
        "--encrypt",
        dest="encrypt",
        action="store_true",  # set to true IF user passes in option --encrypt
        help=_("createextracts.options.encrypt"),
    )
    return parser


# item arguments: datasource, workbook, project, url ...

# Matching classic tabcmd:
# for some reason in parser.project, publish-samples it uses -n for destination project name
# for publish it uses -r for destination project name
# but parser.site uses -r for site-content-url
def set_project_r_arg(parser):
    parser.add_argument("--project", "-r", dest="project_name", default="", help=_("tabcmd.options.project"))
    return parser


def set_project_n_arg(parser):
    parser.add_argument("-n", "--project", dest="project_name", default="", help=_("tabcmd.options.project"))
    return parser


def set_project_arg(parser):
    parser.add_argument("--project", dest="project_name", default="", help=_("tabcmd.options.project"))
    return parser


def set_resource_url_arg(parser):
    parser.add_argument("--url", help=_("tabcmd.options.resource_url"))
    return parser


def set_ds_xor_wb_options(parser):
    target_type_group = parser.add_mutually_exclusive_group(required=False)
    target_type_group.add_argument("-d", "--datasource", action="store_true", help=_("tabcmd.options.datasource"))
    target_type_group.add_argument("-w", "--workbook", action="store_true", help=_("tabcmd.options.workbook"))
    return parser


# pass arguments for either --datasource or --workbook
def set_ds_xor_wb_args(parser, url=False):
    target_type_group = parser.add_mutually_exclusive_group(required=True)
    target_type_group.add_argument("-d", "--datasource", help=_("tabcmd.options.datasource"))
    target_type_group.add_argument("-w", "--workbook", help=_("tabcmd.options.workbook"))
    if url:
        # -U conflicts with --username, they are not case sensitive
        target_type_group.add_argument("--url", help=_("tabcmd.options.resource_url"))
    return parser


def set_description_arg(parser):
    parser.add_argument("-d", "--description", help=_("tabcmd.content.description"))
    return parser


# only in edit-site
def set_site_status_arg(parser):
    parser.add_argument(
        "--status",
        choices=["ACTIVE", "SUSPENDED"],
        type=str.upper,
        help=_("editsite.options.status"),
    )
    return parser


# only in edit-site: flags that map onto TSC SiteItem attributes but are not
# currently wired in create_site_command. Kept out of set_common_site_args so
# createsite --help does not list options its run_command ignores. See #437.
def set_edit_site_only_args(parser):
    # guest access: Classic passes true/false as a string value
    parser.add_argument(
        "-g",
        "--guest-access-enabled",
        choices=["true", "false"],
        help=_("editsite.options.guest_access_enabled"),
    )

    # cache warmup: paired positive/negative boolean, default None so an
    # unpassed flag is a no-op (leaves the server setting unchanged)
    cache_warmup_group = parser.add_mutually_exclusive_group()
    cache_warmup_group.add_argument(
        "--cache-warmup",
        dest="cache_warmup_enabled",
        action="store_true",
        default=None,
        help=_("editsite.options.cache_warmup"),
    )
    cache_warmup_group.add_argument(
        "--no-cache-warmup",
        dest="cache_warmup_enabled",
        action="store_false",
        default=None,
        help=_("editsite.options.no_cache_warmup"),
    )

    # subscription email: also flips custom_subscription_email_enabled
    parser.add_argument(
        "-e",
        "--subscription-email",
        default=None,
        help=_("editsite.options.subscription_email"),
    )

    # subscription footer: also flips custom_subscription_footer_enabled.
    # -f matches Classic tabcmd editsite parity; editsite does not use -f for --filename.
    parser.add_argument(
        "-f",
        "--subscription-footer",
        default=None,
        help=_("editsite.options.subscription_footer"),
    )

    # web extraction: string value, coerced to bool at wire time
    parser.add_argument(
        "--web-extraction-enabled",
        choices=["true", "false"],
        help=_("editsite.options.web_extraction_enabled"),
    )

    # allow subscriptions: inverted onto disable_subscriptions in run_command
    allow_subs_group = parser.add_mutually_exclusive_group()
    allow_subs_group.add_argument(
        "--allow-subscriptions",
        dest="allow_subscriptions",
        action="store_true",
        default=None,
        help=_("editsite.options.allow_subscriptions"),
    )
    allow_subs_group.add_argument(
        "--no-allow-subscriptions",
        dest="allow_subscriptions",
        action="store_false",
        default=None,
        help=_("editsite.options.no_allow_subscriptions"),
    )

    # allow web authoring: direct mapping onto authoring_enabled
    authoring_group = parser.add_mutually_exclusive_group()
    authoring_group.add_argument(
        "--allow-web-authoring",
        dest="allow_web_authoring",
        action="store_true",
        default=None,
        help=_("editsite.options.allow_web_authoring"),
    )
    authoring_group.add_argument(
        "--no-allow-web-authoring",
        dest="allow_web_authoring",
        action="store_false",
        default=None,
        help=_("editsite.options.no_allow_web_authoring"),
    )

    # allow mobile snapshots: maps onto sheet_image_enabled (NOT
    # mobile_biometrics_enabled, which is a separate biometric-auth feature)
    mobile_group = parser.add_mutually_exclusive_group()
    mobile_group.add_argument(
        "--allow-mobile-snapshots",
        dest="allow_mobile_snapshots",
        action="store_true",
        default=None,
        help=_("editsite.options.allow_mobile_snapshots"),
    )
    mobile_group.add_argument(
        "--no-allow-mobile-snapshots",
        dest="allow_mobile_snapshots",
        action="store_false",
        default=None,
        help=_("editsite.options.no_allow_mobile_snapshots"),
    )

    # time zone: string value, mutually exclusive with --use-default-time-zone
    tz_group = parser.add_mutually_exclusive_group()
    tz_group.add_argument(
        "--time-zone",
        default=None,
        help=_("editsite.options.time_zone"),
    )
    tz_group.add_argument(
        "--use-default-time-zone",
        action="store_true",
        default=None,
        help=_("editsite.options.use_default_time_zone"),
    )
    return parser


# mismatched arguments: createsite says --url, editsite says --site-id
# just let both commands use either of them
def set_site_id_args(parser):
    site_id = parser.add_mutually_exclusive_group()
    site_id.add_argument("--site-id", help=_("tabcmd.content.site_id"))
    site_id.add_argument("-r", "--url", help=_("tabcmd.content.site_id"))
    return parser


# create-site/update-site - lots of these options are never used elsewhere
def set_common_site_args(parser):

    parser = set_site_id_args(parser)

    parser.add_argument("--user-quota", type=int, help=_("createsite.options.user-quota"))

    set_site_mode_option(parser)

    parser.add_argument(
        "--storage-quota",
        type=int,
        help=_("createsite.options.storage-quota"),
    )

    encryption_modes = ["enforced", "enabled", "disabled"]
    parser.add_argument(
        "--extract-encryption-mode",
        choices=encryption_modes,
        type=case_insensitive_string_type(encryption_modes),
        help=_("editsite.options.extract_encryption_mode"),
    )

    parser.add_argument(
        "--run-now-enabled",
        choices=["true", "false"],
        help=_("editsite.options.run_now_enabled"),
    )
    return parser


def set_site_mode_option(parser):
    site_group = parser.add_mutually_exclusive_group()
    site_group.add_argument(
        "--site-mode",
        dest="site_admin_user_management",
        action="store_true",
        help=_("createsite.options.site-mode"),
    )
    site_group.add_argument(
        "--no-site-mode",
        dest="site_admin_user_management",
        action="store_false",
        help=_("createsite.options.site-mode"),
    )


# this option is only used by listsites
def set_site_detail_option(parser):
    parser.add_argument(
        "--get-extract-encryption-mode",
        action="store_true",
        help=_("listsites.options.get_extract_encryption_mode"),
    )


def set_destination_filename_arg(parser):
    parser.add_argument("-f", "--filename", help=_("get.options.file"))


def set_publish_args(parser):
    parser.add_argument("-n", "--name", help=_("publish.options.name"))

    creds = parser.add_mutually_exclusive_group()
    creds.add_argument("--oauth-username", help=_("publish.options.oauth-username"))
    creds.add_argument("--db-username", help=_("publish.options.db-username"))
    parser.add_argument("--save-oauth", action="store_true", help=_("publish.options.save-oauth"))

    parser.add_argument("--db-password", help=_("publish.options.db-password"))
    parser.add_argument("--save-db-password", action="store_true", help=_("publish.options.save-db-password"))

    parser.add_argument("--tabbed", action="store_true", help=_("tabcmd.publish.options.tabbed.detailed"))
    parser.add_argument("--disable-uploader", action="store_true", help=_("tabcmd.options.deprecated"))

    parser.add_argument("--restart", help=_("publish.options.restart"))
    parser.add_argument("--encrypt-extracts", action="store_true", help=_("publish.options.encrypt_extracts"))
    parser.add_argument(
        "--skip-connection-check",
        action="store_true",
        help=_("tabcmd.global.help.skip_connection_check"),
    )

    thumbnails = parser.add_mutually_exclusive_group()
    thumbnails.add_argument("--thumbnail-username", help=_("publish.options.thumbnail-username"))
    thumbnails.add_argument("--thumbnail-group", help=_("publish.options.thumbnail-groupname"))

    parser.add_argument("--use-tableau-bridge", action="store_true", help=_("tabcmd.refresh.options.bridge"))


# these two are used to publish an extract to an existing data source
def set_append_replace_option(parser):
    append_group = parser.add_mutually_exclusive_group()
    append_group.add_argument("--append", action="store_true", help=_("tabcmd.publish.options.append.detailed"))

    # This will keep the metadata of the existing data source and replace the data in the extract file
    # This is meant for when a) the local file is an extract b) the server item is an existing data source
    append_group.add_argument("--replace", action="store_true", help=_("publish.options.replace"))


# This will overwrite the metadata and data of the existing content
def set_overwrite_option(parser):
    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help=_("publish.options.overwrite"),
    )


# refresh-extracts
def set_incremental_options(parser):
    parser.add_argument("--incremental", action="store_true", help=_("refreshextracts.options.incremental"))
    return parser


def set_sync_wait_options(parser):
    parser.add_argument("--synchronous", action="store_true", help=_("refreshextracts.options.synchronous"))
    return parser


def set_calculations_options(parser):
    calc_group = parser.add_mutually_exclusive_group()
    calc_group.add_argument(
        "--addcalculations",
        action="store_true",
        help=_("tabcmd.options.deprecated"),
    )
    calc_group.add_argument(
        "--removecalculations",
        action="store_true",
        help=_("tabcmd.options.deprecated"),
    )
    return calc_group


# TODO below
# these are not used in any Online operations, on the backburner

# edit-domain: none of these are used in other commands
# def set_domain_arguments(parser):
#     parser.add_argument(
#         "--id",
#         help="The ID of domain to change. To get a list of domain IDs, use use listdomains.",
#     )
#     parser.add_argument("--name", help="The new name for the domain.")
#     parser.add_argument("--nickname", help="The new nickname for the domain.")
#     return parser


# set setting
# choices: allow_scheduling, embedded_credentials, remember_passwords_forever
# use !setting-name to disable them
# hmmmm


# sync-group
# license_modes = ["on-login", "on-sync"]


# def set_update_group_args(parser):
#     parser.add_argument(
#         "--grant-license-mode",
#         choices=license_modes,
#         type=case_insensitive_string_type(license_modes),
#         help="Specifies whether a role should be granted on sign in. ",
#     )
#     parser.add_argument(
#         "--overwritesiterole",
#         action="store_true",
#         help="Allows a user’s site role to be overwritten with a less privileged one when using --role.",
#     )
#     return parser
