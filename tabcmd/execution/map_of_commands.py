from tabcmd.commands.auth.login_command import *
from tabcmd.commands.auth.logout_command import *
from tabcmd.commands.datasources_and_workbooks.delete_command import *
from tabcmd.commands.datasources_and_workbooks.export_command import *
from tabcmd.commands.datasources_and_workbooks.get_url_command import *
from tabcmd.commands.datasources_and_workbooks.publish_command import *
from tabcmd.commands.extracts.create_extracts_command import *
from tabcmd.commands.extracts.decrypt_extracts_command import *
from tabcmd.commands.extracts.delete_extracts_command import *
from tabcmd.commands.extracts.encrypt_extracts_command import *
from tabcmd.commands.extracts.reencrypt_extracts_command import *
from tabcmd.commands.extracts.refresh_extracts_command import *
from tabcmd.commands.group.create_group_command import *
from tabcmd.commands.group.delete_group_command import *
from tabcmd.commands.help.help_command import *
from tabcmd.commands.project.create_project_command import *
from tabcmd.commands.project.delete_project_command import *
from tabcmd.commands.project.publish_samples_command import *
from tabcmd.commands.site.create_site_command import *
from tabcmd.commands.site.delete_site_command import *
from tabcmd.commands.site.edit_site_command import *
from tabcmd.commands.site.list_sites_command import *
from tabcmd.commands.user.add_users_command import *
from tabcmd.commands.user.create_site_users import *
from tabcmd.commands.user.delete_site_users_command import *

# from tabcmd.commands.user.create_users import *
from tabcmd.commands.user.remove_users_command import *

from tabcmd.parsers.add_users_parser import *
from tabcmd.parsers.create_extracts_parser import *
from tabcmd.parsers.create_group_parser import *
from tabcmd.parsers.create_project_parser import *
from tabcmd.parsers.create_site_parser import *
from tabcmd.parsers.create_site_users_parser import *

# from tabcmd.parsers.create_users_parser import *
from tabcmd.parsers.decrypt_extracts_parser import *
from tabcmd.parsers.delete_extracts_parser import *
from tabcmd.parsers.delete_group_parser import *
from tabcmd.parsers.delete_parser import *
from tabcmd.parsers.delete_project_parser import *
from tabcmd.parsers.delete_site_parser import *
from tabcmd.parsers.delete_site_users_parser import *
from tabcmd.parsers.edit_site_parser import *
from tabcmd.parsers.encrypt_extracts_parser import *
from tabcmd.parsers.export_parser import *
from tabcmd.parsers.get_url_parser import *
from tabcmd.parsers.help_parser import *
from tabcmd.parsers.list_sites_parser import *
from tabcmd.parsers.login_parser import *
from tabcmd.parsers.logout_parser import *
from tabcmd.parsers.publish_parser import *
from tabcmd.parsers.publish_samples_parser import *
from tabcmd.parsers.reencrypt_parser import *
from tabcmd.parsers.refresh_extracts_parser import *
from tabcmd.parsers.remove_users_parser import *

from typing import Callable, List


class CommandsMap:
    commands_hash_map: List[tuple[str, Callable, str]] = [
        # not yet implemented "createusers": ("createusers", CreateUserCommand, "Create users on the server"),
        # run schedule
        ("addusers", AddUserCommand, "Add users to a group", AddUserParser.add_user_parser),
        (
            "createextracts",
            CreateExtracts,
            "Create extracts for a published workbook or data source",
            CreateExtractsParser.create_extracts_parser,
        ),
        ("creategroup", CreateGroupCommand, "Create a local group", CreateGroupParser.create_group_parser),
        ("createproject", CreateProjectCommand, "Create a project", CreateProjectParser.create_project_parser),
        ("createsite", CreateSiteCommand, "Create a site", CreateSiteParser.create_site_parser),
        (
            "createsiteusers",
            CreateSiteUsersCommand,
            "Create users on the current site",
            CreateSiteUsersParser.create_site_user_parser,
        ),
        (
            "decryptextracts",
            DecryptExtracts,
            "Decrypt extracts on a site",
            DecryptExtractsParser.decrypt_extracts_parser,
        ),
        ("delete", DeleteCommand, "Delete a workbook or data source from the server", DeleteParser.delete_parser),
        (
            "deleteextracts",
            DeleteExtracts,
            "Delete extracts for a published workbook or data source",
            DeleteExtractsParser.delete_extracts_parser,
        ),
        ("deletegroup", DeleteGroupCommand, "Delete a group", DeleteGroupParser.delete_group_parser),
        ("deleteproject", DeleteProjectCommand, "Delete a project", DeleteProjectParser.delete_project_parser),
        ("deletesite", DeleteSiteCommand, "Delete a site", DeleteSiteParser.delete_site_parser),
        (
            "deletesiteusers",
            DeleteSiteUsersCommand,
            "Delete site users",
            DeleteSiteUsersParser.delete_site_users_parser,
        ),
        ("editsite", EditSiteCommand, "Edit a site", EditSiteParser.edit_site_parser),
        (
            "encryptextracts",
            EncryptExtracts,
            "Encrypt extracts on a site",
            EncryptExtractsParser.encrypt_extracts_parser,
        ),
        ("export", ExportCommand, "Export the data or image of a view from the server", ExportParser.export_parser),
        ("get", GetUrl, "Get a file from the server", GetUrlParser.get_url_parser),
        ("help", HelpCommand, "Show help and exit", HelpParser.help_parser),
        ("listsites", ListSiteCommand, "List sites for user", ListSitesParser.list_site_parser),
        ("login", LoginCommand, "Log in to site", LoginParser.login_parser),
        ("logout", LogoutCommand, "Sign out from the server", LogoutParser.logout_parser),
        (
            "publish",
            PublishCommand,
            "Publish a workbook, data source, or extract to the server",
            PublishParser.publish_parser,
        ),
        (
            "publishsamples",
            PublishSamplesCommand,
            "publish samples to the server",
            PublishSamplesParser.publish_samples_parser,
        ),
        (
            "reencryptextracts",
            ReencryptExtracts,
            "Reencrypt extracts on a site",
            ReencryptExtractsParser.reencrypt_extracts_parser,
        ),
        (
            "refreshextracts",
            RefreshExtracts,
            "Refresh the extracts of a workbook or datasource on the server",
            RefreshExtractsParser.refresh_extracts_parser,
        ),
        ("removeusers", RemoveUserCommand, "Remove users from a group", RemoveUserParser.remove_user_parser),
    ]
