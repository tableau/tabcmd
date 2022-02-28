import argparse

"""
Basics of options
- if not otherwise specified, the value passed in with the option will be saved as args.option-name
- all arguments in here are optional: names must be --option-name so users can tell it's optional
- options that just need to turn on or off a flag should be set with action=store_True/False
Method naming conventions
- I have named methods in here aaaa_arg if it returns a value we want, aaa_option if it's a flag
- all methods in here should return a parser for nice fluent chaining

All these options can be used with any command.
Options are listed here in the same order as the 'global options' list online at
https://help.tableau.com/current/server/en-us/tabcmd_cmd.htm#options7

Ideally *all* options would be in here, so they can be kept updated together and simply listed on the
relevant parser
"""


def evaluate_project_path(path):
    last_index = 1
    second_last_index = 2
    """ Method to parse the project path provided by the user"""
    first_dir_from_end = None
    if path[-last_index] != "/":
        path = path + "/"
    new_path = path.rsplit("/")[-second_last_index]
    for directory in new_path[::-last_index]:
        if directory != " ":
            first_dir_from_end = new_path
            break
    return first_dir_from_end


def set_parent_project_arg(parser):
    parser.add_argument(
        "--parent-project-path", default=None, help="path of parent project"
    )
    return parser


# add/remove-user
# parser.users command has a bunch of deprecated options. Just ditch them?
# --admin-type, --[no-]publisher, --[no-]complete (which was ssuuuuubtly different from add-users)


def set_users_file_arg(parser):
    parser.add_argument(
        "--users",
        required=True,
        type=argparse.FileType("r", encoding="UTF-8"),
        help="CSV file containing a list of users.",
    )
    return parser


def set_users_file_positional(parser):
    parser.add_argument(
        "filename",
        metavar="filename.csv",
        type=argparse.FileType("r", encoding="UTF-8"),
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


def set_role_arg(parser):
    parser.add_argument(
        "-r",
        "--role",
        choices=[
            "ServerAdministrator",
            "SiteAdministratorCreator",
            "SiteAdministratorExplorer",
            "SiteAdministrator",
            "Creator",
            "ExplorerCanPublish",
            "Publisher",
            "Explorer",
            "Interactor",
            "Viewer",
            "Unlicensed",
        ],
        help="Specifies a site role for all users in the .csv file.",
    )
    return parser


def set_silent_option(parser):
    parser.add_argument(
        "--silent-progress", help="Do not display progress messages for the command."
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
# docs don't say it, but --embedded-datasources and --include-all could be mutually exclusive
def set_embedded_datasources_options(parser):
    embedded_group = parser.add_mutually_exclusive_group()
    embedded_group.add_argument(
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
        dest="encrypt_extract",
        action="store_false",
        help="Encrypt the newly created extract.",
    )
    return parser


# item arguments: datasource, workbook, project, url ...
# distinct from all the positional 'name' arguments for e.g deleteproject


# for some reason in parser.project, publish-samples it uses -n for destination project name
# for publish it uses -r for destination project name
# but parser.site uses -r for site-content-url
def set_project_r_arg(parser):
    parser.add_argument(
        "--project",
        "-r",
        dest="projectname",
        default="",
        help="The name of the project.",
    )
    return parser


def set_project_n_arg(parser):
    parser.add_argument(
        "--project",
        "-n",
        dest="projectname",
        default="",
        help="The name of the project.",
    )
    return parser


def set_project_arg(parser):
    parser.add_argument(
        "--project", dest="projectname", default="", help="The name of the project."
    )
    return parser


# the help message for 'datasource' needs to be slightly different for each command
def set_datasource_arg(parser):
    parser.add_argument(
        "--datasource", "-d", help="The name of the target data source."
    )
    return parser


def set_site_url_arg(parser):
    parser.add_argument(
        "--url", help="The canonical name for the resource as it appears in the URL"
    )
    return parser


def set_workbook_arg(parser):
    parser.add_argument("--workbook", "-w", help="The name of the target workbook.")
    return parser


def set_ds_xor_wb_args(parser):
    target_type_group = parser.add_mutually_exclusive_group(required=True)
    target_type_group.add_argument(
        "-d", "--datasource", help="The name of the target datasource."
    )
    target_type_group.add_argument(
        "-w", "--workbook", help="The name of the target workbook."
    )
    return parser


def set_description_arg(parser):
    parser.add_argument(
        "--description", "-d", help="Specifies a description for the item."
    )
    return parser


# create-site/update-site - lots of these options are never used elsewhere
def set_content_url_arg(parser):
    parser.add_argument(
        "--url",
        "-r",
        help="Used in URLs to specify the site. Different from the site name.",
    )
    return parser


# BUT this seems to be a mismatch between them? site id is listed in edit-site
def set_site_id_arg(parser):
    parser.add_argument(
        "--site-id", help="Used in the URL to uniquely identify the site."
    )
    return parser


# only in edit-site
def set_site_status_arg(parser):
    parser.add_argument(
        "--status",
        choices=["ACTIVE", "SUSPENDED"],
        help="Set to ACTIVE to activate a site, or to SUSPENDED to suspend a site.",
    )
    return parser


# these options are all shared in create-site and edit-site
def set_site_args(parser):
    parser.add_argument(
        "--user-quota", help="Maximum number of users that can be added to the site."
    )

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

    parser.add_argument(
        "--storage-quota",
        help="In MB, the amount of data that can be stored on the site.",
    )

    parser.add_argument(
        "--extract-encryption-mode",
        choices=["enforced", "enabled", "disabled"],
        help="The extract encryption mode for the site can be enforced, enabled or disabled. ",
    )

    parser.add_argument(
        "--run-now-enabled",
        help="Allow or deny users from running extract refreshes, flows, or schedules manually. \
            true to allow users to run tasks manually or false to prevent users from running tasks manually.",
    )
    return parser


# this option is only used by listsites
def set_view_site_encryption(parser):
    parser.add_argument(
        "--get-extract-encryption-mode",
        action="store_true",
        help="Include the extract encryption mode for each site.",
    )


# export --- mmmaaaannnyyyy options
def set_filename_arg(parser):
    parser.add_argument(
        "-f", "--filename", help="Saves the file with the given filename and extension."
    )


def set_publish_args(parser):
    parser.add_argument(
        "-n", "--name", help="Name to publish the new datasource or workbook by."
    )

    append_group = parser.add_mutually_exclusive_group()
    append_group.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="Overwrites the workbook, data source, or data extract if it already exists on the server.",
    )
    append_group.add_argument(
        "--append",
        action="store_true",
        help="Append the extract file to the existing data source.",
    )
    parser.add_argument(
        "--db-username",
        help="Use this option to publish a database user name with the workbook, data source, or data extract.",
    )
    parser.add_argument(
        "--db-password",
        help="publish a database password with the workbook, data source, or extract",
    )
    parser.add_argument(
        "--save-db-password",
        help="Stores the provided database password on the server.",
    )
    parser.add_argument(
        "--tabbed",
        action="store_true",
        help="When a workbook with tabbed views is published, each sheet becomes a tab that viewers can use to \
        navigate through the workbook",
    )
    parser.add_argument(
        "--replace", help="Use the extract file to replace the existing data source."
    )
    parser.add_argument(
        "--disable-uploader", help="Disable the incremental file uploader."
    )
    parser.add_argument("--restart", help="Restart the file upload.")
    parser.add_argument(
        "--encrypt-extracts",
        help="Encrypt extracts in the workbook, datasource, or extract being published to the server",
    )
    parser.add_argument(
        "--oauth-username", help="The email address of a preconfigured OAuth connection"
    )
    parser.add_argument("--save-oauth")
    parser.add_argument("--thumbnail-username")
    parser.add_argument("--thumbnail-group")  # not implemented in the REST API


# refresh-extracts
def set_incremental_options(parser):
    sync_group = parser.add_mutually_exclusive_group()
    sync_group.add_argument(
        "--incremental", help="Runs the incremental refresh operation."
    )
    sync_group.add_argument(
        "--synchronous",
        help="Adds the full refresh operation to the queue used by the Backgrounder process, to be run as soon as a \
        Backgrounder process is available.",
    )
    return parser


def set_calculations_options(parser):
    calc_group = parser.add_mutually_exclusive_group()
    calc_group.add_argument(
        "--addcalculations",
        action="store_true",
        help="Add precalculated data operations in the extract data source.",
    )
    calc_group.add_argument(
        "--removecalculations",
        action="store_true",
        help="Remove precalculated data in the extract data source.",
    )
    return parser


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
    target_users_group.add_argument(
        "--target-username", help="Clears sub value for the specified individual user."
    )
    target_users_group.add_argument("--all", help="Clears sub values for all users.")
    return parser


# set setting
# choices: allow_scheduling, embedded_credentials, remember_passwords_forever
# use !setting-name to disable them
# hmmmm


# sync-group
def set_update_group_args(parser):
    parser.add_argument(
        "--grant-license-mode",
        choices=["on-login", "on-sync"],
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
