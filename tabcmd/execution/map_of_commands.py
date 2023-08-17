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
from tabcmd.commands.user.remove_users_command import *
from tabcmd.commands.site.list_command import *
from tabcmd.commands.auth.version_command import *


class CommandsMap:
    commands_hash_map = [
        # not yet implemented "createusers": ("createusers", CreateUserCommand, "Create users on the server"),
        # run schedule
        AddUserCommand,
        CreateExtracts,
        CreateGroupCommand,
        CreateProjectCommand,
        CreateSiteCommand,
        CreateSiteUsersCommand,
        DecryptExtracts,
        DeleteCommand,
        DeleteExtracts,
        DeleteGroupCommand,
        DeleteProjectCommand,
        DeleteSiteCommand,
        DeleteSiteUsersCommand,
        EditSiteCommand,
        EncryptExtracts,
        ExportCommand,
        GetUrl,
        ListSiteCommand,
        ListCommand,
        LoginCommand,
        LogoutCommand,
        PublishCommand,
        PublishSamplesCommand,
        ReencryptExtracts,
        RefreshExtracts,
        RemoveUserCommand,
        VersionCommand,
    ]
