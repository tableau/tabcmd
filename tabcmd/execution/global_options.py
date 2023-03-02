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
    parser.add_argument("--parent-project-path", default=None, help="path of parent project")
    return parser


# add/remove-user
# parser.users command has a bunch of deprecated options. Just ditch them?
# --admin-type, --[no-]publisher, --[no-]complete (which was ssuuuuubtly different from add-users)


def set_users_file_arg(parser):
    parser.add_argument(
        "--users",
        required=True,
        type=argparse.FileType("r", encoding="utf-8-sig"),
        help="CSV file containing a list of users.",
    )
    return parser


def set_users_file_positional(parser):
    parser.add_argument(
        "filename",
        metavar="filename.csv",
        type=argparse.FileType("r", encoding="utf-8-sig"),
        help="CSV file containing a list of users.",
    )
    return parser


def set_no_wait_option(parser):
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Do not wait for asynchronous jobs to complete.",
    )
    return parser


def set_silent_option(parser):
    parser.add_argument(
        "--silent-progress", action="store_true", help="Do not display progress messages for the command."
    )
    return parser


def set_completeness_options(parser):
    completeness_group = parser.add_mutually_exclusive_group()
    completeness_group.add_argument(
        "--complete",
        dest="require_all_valid",
        action="store_true",
        help="Requires that all rows be valid for any change to succeed.",
    )
    completeness_group.add_argument(
        "--no-complete",
        dest="require_all_valid",
        action="store_false",
        help="Allows a change to succeed when not all rows are valid. If not specified --complete is used.",
    )
    completeness_group.set_defaults(require_all_valid=True)
    return parser


# used in create/delete extract
def set_embedded_datasources_options(parser):
    # one of these is required IFF we are using a workbook instead of datasource
    embedded_group = parser.add_mutually_exclusive_group()
    embedded_group.add_argument(  # nargs?
        "--embedded-datasources",
        help="A space-separated list of embedded data source names within the target workbook.",
    )
    embedded_group.add_argument(
        "--include-all",
        action="store_true",
        help="Include all embedded data sources within target workbook.",
    )
    return parser


# used in create extract. listed in delete-extract but makes no sense there
def set_encryption_option(parser):
    parser.add_argument(
        "--encrypt",
        dest="encrypt",
        action="store_true",  # set to true IF user passes in option --encrypt
        help="Encrypt the newly created extract. [N/a on Tableau Cloud: extract encryption is controlled by Site Admin]",
    )
    return parser


# item arguments: datasource, workbook, project, url ...

# for some reason in parser.project, publish-samples it uses -n for destination project name
# for publish it uses -r for destination project name
# but parser.site uses -r for site-content-url
def set_project_r_arg(parser):
    parser.add_argument(
        "--project",
        "-r",
        dest="project_name",
        default="",
        help="The name of the project.",
    )
    return parser


def set_project_n_arg(parser):
    parser.add_argument(
        "-n",
        "--project",
        dest="project_name",
        default="",
        help="The name of the project.",
    )
    return parser


def set_project_arg(parser):
    parser.add_argument("--project", dest="project_name", default="", help="The name of the project.")
    return parser


def set_ds_xor_wb_options(parser):
    target_type_group = parser.add_mutually_exclusive_group(required=False)
    target_type_group.add_argument("-d", "--datasource", action="store_true", help="The name of the target datasource.")
    target_type_group.add_argument("-w", "--workbook", action="store_true", help="The name of the target workbook.")
    return parser


# pass arguments for either --datasource or --workbook
def set_ds_xor_wb_args(parser, url=False):
    target_type_group = parser.add_mutually_exclusive_group(required=True)
    target_type_group.add_argument("-d", "--datasource", help="The name of the target datasource.")
    target_type_group.add_argument("-w", "--workbook", help="The name of the target workbook.")
    if url:
        # -U conflicts with --username, they are not case sensitive
        target_type_group.add_argument("--url", help=_("deleteextracts.options.url"))
    return parser


def set_description_arg(parser):
    parser.add_argument("-d", "--description", help="Specifies a description for the item.")
    return parser


# only in edit-site
def set_site_status_arg(parser):
    parser.add_argument(
        "--status",
        choices=["ACTIVE", "SUSPENDED"],
        type=str.upper,
        help="Set to ACTIVE to activate a site, or to SUSPENDED to suspend a site.",
    )
    return parser


# mismatched arguments: createsite says --url, editsite says --site-id
# just let both commands use either of them
def set_site_id_args(parser):
    site_id = parser.add_mutually_exclusive_group()
    site_id.add_argument("--site-id", help="Used in the URL to uniquely identify the site.")
    site_id.add_argument(
        "-r",
        "--url",
        help="Used in URLs to specify the site. Different from the site name.",
    )
    return parser


# create-site/update-site - lots of these options are never used elsewhere
def set_common_site_args(parser):

    parser = set_site_id_args(parser)

    parser.add_argument("--user-quota", type=int, help="Maximum number of users that can be added to the site.")

    set_site_mode_option(parser)

    parser.add_argument(
        "--storage-quota",
        type=int,
        help="In MB, the amount of data that can be stored on the site.",
    )

    encryption_modes = ["enforced", "enabled", "disabled"]
    parser.add_argument(
        "--extract-encryption-mode",
        choices=encryption_modes,
        type=case_insensitive_string_type(encryption_modes),
        help="The extract encryption mode for the site can be enforced, enabled or disabled. "
             "[N/a on Tableau Cloud: encryption mode is always enforced] ",
    )

    parser.add_argument(
        "--run-now-enabled",
        choices=["true", "false"],
        help="Allow or deny users from running extract refreshes, flows, or schedules manually.",
    )
    return parser


def set_site_mode_option(parser):
    site_help = "Allows or denies site administrators the ability to add users to or remove users from the site."
    site_group = parser.add_mutually_exclusive_group()
    site_group.add_argument(
        "--site-mode",
        dest="site_admin_user_management",
        action="store_true",
        help=site_help,
    )
    site_group.add_argument(
        "--no-site-mode",
        dest="site_admin_user_management",
        action="store_false",
        help=site_help,
    )


# this option is only used by listsites
def set_site_detail_option(parser):
    parser.add_argument(
        "--get-extract-encryption-mode",
        action="store_true",
        help="Include the extract encryption mode for each site.",
    )


# export --- mmmaaaannnyyyy options
def set_filename_arg(parser, description=_("get.options.file")):
    parser.add_argument("-f", "--filename", help=description)


def set_publish_args(parser):
    parser.add_argument("-n", "--name", help="Name to publish the new datasource or workbook by.")

    creds = parser.add_mutually_exclusive_group()
    creds.add_argument("--oauth-username", help="The email address of a preconfigured OAuth connection")
    creds.add_argument(
        "--db-username",
        help="Use this option to publish a database user name with the workbook, data source, or data extract.",
    )
    parser.add_argument("--save-oauth", action="store_true", help="Save embedded OAuth credentials in the datasource")

    parser.add_argument(
        "--db-password",
        help="publish a database password with the workbook, data source, or extract",
    )
    parser.add_argument(
        "--save-db-password",
        action="store_true",
        help="Stores the provided database password on the server.",
    )

    parser.add_argument(
        "--tabbed",
        action="store_true",
        help="When a workbook with tabbed views is published, each sheet becomes a tab that viewers can use to \
        navigate through the workbook",
    )
    parser.add_argument("--disable-uploader", action="store_true", help="[DEPRECATED - has no effect] Disable the incremental file uploader.")
    parser.add_argument("--restart", help="[DEPRECATED - has no effect] Restart the file upload.")
    parser.add_argument(
        "--encrypt-extracts",
        action="store_true",
        help="Encrypt extracts in the workbook, datasource, or extract being published to the server. "
             "[N/a on Tableau Cloud: extract encryption is controlled by Site Admin]",
    )

    # These two only apply for a workbook, not a datasource
    thumbnails = parser.add_mutually_exclusive_group()
    thumbnails.add_argument(
        "--thumbnail-username",
        help="If the workbook contains user filters, the thumbnails will be generated based on what the "
             "specified user can see. Cannot be specified when --thumbnail-group option is set.")
    thumbnails.add_argument(
        "--thumbnail-group",
        help="[Not yet implemented] If the workbook contains user filters, the thumbnails will be generated based on what the "
             "specified group can see. Cannot be specified when --thumbnail-username option is set.")

    parser.add_argument("--use-tableau-bridge", action="store_true", help="Refresh datasource through Tableau Bridge")


# these two are used to publish an extract to an existing data source
def set_append_replace_option(parser):
    append_group = parser.add_mutually_exclusive_group()
    append_group.add_argument(
        "--append",
        action="store_true",
        help="Set to true to append the data being published to an existing data source that has the same name. "
             "The default behavior is to fail if the data source already exists. "
             "If append is set to true but the data source doesn't already exist, the operation fails."
    )

    # what's the difference between this and 'overwrite'?
    # This is meant for when a) the local file is an extract b) the server item is an existing data source
    append_group.add_argument(
        "--replace",
        action="store_true",
        help="Use the extract file being published to replace data in the existing data source. The default "
             "behavior is to fail if the item already exists."
    )

# this is meant to be like replacing like
def set_overwrite_option(parser):
    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="Overwrites the workbook, data source, or data extract if it already exists on the server. The default "
             "behavior is to fail if the item already exists."
    )


# refresh-extracts
def set_incremental_options(parser):
    sync_group = parser.add_mutually_exclusive_group()
    sync_group.add_argument("--incremental", action="store_true", help="Runs the incremental refresh operation.")
    sync_group.add_argument(
        "--synchronous",
        action="store_true",
        help="Adds the full refresh operation to the queue used by the Backgrounder process, to be run as soon as a \
        Backgrounder process is available.",
    )
    return parser


def set_calculations_options(parser):
    calc_group = parser.add_mutually_exclusive_group()
    calc_group.add_argument(
        "--addcalculations",
        action="store_true",
        help="[Not implemented] Add precalculated data operations in the extract data source.",
    )
    calc_group.add_argument(
        "--removecalculations",
        action="store_true",
        help="[Not implemented] Remove precalculated data in the extract data source.",
    )
    return calc_group


# TODO below
# these are not used in any Online operations, on the backburner


# edit-domain: none of these are used in other commands
def set_domain_arguments(parser):
    parser.add_argument(
        "--id",
        help="The ID of domain to change. To get a list of domain IDs, use use listdomains.",
    )
    parser.add_argument("--name", help="The new name for the domain.")
    parser.add_argument("--nickname", help="The new nickname for the domain.")
    return parser


# reset-openid-sub
def set_target_users_arg(parser):
    target_users_group = parser.add_mutually_exclusive_group()
    target_users_group.add_argument("--target-username", help="Clears sub value for the specified individual user.")
    target_users_group.add_argument("--all", action="store_true", help="Clears sub values for all users.")
    return parser


# set setting
# choices: allow_scheduling, embedded_credentials, remember_passwords_forever
# use !setting-name to disable them
# hmmmm


# sync-group
license_modes = ["on-login", "on-sync"]


def set_update_group_args(parser):
    parser.add_argument(
        "--grant-license-mode",
        choices=license_modes,
        type=case_insensitive_string_type(license_modes),
        help="Specifies whether a role should be granted on sign in. ",
    )
    parser.add_argument(
        "--overwritesiterole",
        action="store_true",
        help="Allows a user’s site role to be overwritten with a less privileged one when using --role.",
    )
    return parser


def set_upgrade_stop_option(parser):
    parser.add_argument(
        "--stop",
        action="store_true",
        help="When specified, stops the in progress Upgrade Thumbnails job.",
    )
    return parser


# validate-idp-metadata
# TODO not sure how these space-separated lists will work
def set_validate_idp_options(parser):
    parser.add_argument(
        "--digest-algorithms",
        metavar="<ALGORITHMS>",
        help="A space-separated list of digest algorithms. Legal values are sha1and sha256. \
            If not specified, server uses values from server configuration setting, \
            wgserver.saml.blocklisted_digest_algorithms.",
    )
    parser.add_argument(
        "--min-allowed-elliptic-curve-size",
        metavar="<SIZE>",
        help="If not specified, server uses values from server configuration setting, \
        wgserver.saml.min_allowed.elliptic_curve_size.",
    )
    parser.add_argument(
        "--min-allowed-rsa-key-size",
        metavar="<SIZE>",
        help="If not specified, server uses values from server configuration setting, \
        wgserver.saml.min_allowed.rsa_key_size.",
    )
    parser.add_argument(
        "--site-names",
        metavar="<SITENAMES>",
        help="A space-separated list of site names on which to perform certificate validation. \
        If not specified, then all sites are inspected.",
    )
