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
from tabcmd.commands.project.publish_samples_command import PublishSamplesCommand
from tabcmd.commands.site.create_site_command import *
from tabcmd.commands.site.delete_site_command import *
from tabcmd.commands.site.edit_site_command import *
from tabcmd.commands.site.list_sites_command import *
from tabcmd.commands.user.add_users_command import *
from tabcmd.commands.user.create_site_users import *
from tabcmd.commands.user.delete_site_users_command import *

# from tabcmd.commands.user.create_users import *
from tabcmd.commands.user.remove_users_command import *


class CommandsMap:
    commands_hash_map = {
        "login": ("login", LoginCommand, "Sign in to the server"),
        "logout": ("logout", LogoutCommand, "Sign out from the server"),
        "delete": (
            "delete",
            DeleteCommand,
            "Delete a workbook or data source from the server",
        ),
        "export": (
            "export",
            ExportCommand,
            "Export the data or image of a view from the server",
        ),
        "get": ("get", GetUrl, "Get a file from the server"),
        "publish": (
            "publish",
            PublishCommand,
            "Publish a workbook, data source, or extract to the server",
        ),
        # run schedule
        "createextracts": (
            "createextracts",
            CreateExtracts,
            "Create extracts for a published workbook or data source",
        ),
        "decryptextracts": (
            "decryptextracts",
            DecryptExtracts,
            "Decrypt extracts on a site",
        ),
        "deleteextracts": (
            "deleteextracts",
            DeleteExtracts,
            "Delete extracts for a published workbook or data source",
        ),
        "encryptextracts": (
            "encryptextracts",
            EncryptExtracts,
            "Encrypt extracts on a site",
        ),
        "reencryptextracts": (
            "reencryptextracts",
            ReencryptExtracts,
            "Reencrypt extracts on a site",
        ),
        "refreshextracts": (
            "refreshextracts",
            RefreshExtracts,
            "Refresh the extracts of a workbook or datasource on the server",
        ),
        "creategroup": ("creategroup", CreateGroupCommand, "Create a local group"),
        "deletegroup": ("deletegroup", DeleteGroupCommand, "Delete a group"),
        "createproject": ("createproject", CreateProjectCommand, "Create a project"),
        "deleteproject": ("deleteproject", DeleteProjectCommand, "Delete a project"),
        "publishsamples": (
            "publishsamples",
            PublishSamplesCommand,
            "publish samples to the server",
        ),
        "createsite": ("createsite", CreateSiteCommand, "Create a site"),
        "deletesite": ("deletesite", DeleteSiteCommand, "Delete a site"),
        "editsite": ("editsite", EditSiteCommand, "Edit a site"),
        "listsites": ("listsites", ListSiteCommand, "List sites for user"),
        # not yet implemented "createusers": ("createusers", CreateUserCommand, "Create users on the server"),
        "addusers": ("addusers", AddUserCommand, "Add users to a group"),
        "createsiteusers": (
            "createsiteusers",
            CreateSiteUsersCommand,
            "Create users on the current site",
        ),
        "deletesiteusers": (
            "deletesiteusers",
            DeleteSiteUsersCommand,
            "Delete site users",
        ),
        "removeusers": ("removeusers", RemoveUserCommand, "Remove users from a group"),
        "help": ("help", HelpCommand, "Show help and exit"),
    }
