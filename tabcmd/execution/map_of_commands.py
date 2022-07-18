from src.commands.auth.login_command import *
from src.commands.auth.logout_command import *
from src.commands.datasources_and_workbooks.delete_command import *
from src.commands.datasources_and_workbooks.export_command import *
from src.commands.datasources_and_workbooks.get_url_command import *
from src.commands.datasources_and_workbooks.publish_command import *
from src.commands.extracts.create_extracts_command import *
from src.commands.extracts.decrypt_extracts_command import *
from src.commands.extracts.delete_extracts_command import *
from src.commands.extracts.encrypt_extracts_command import *
from src.commands.extracts.reencrypt_extracts_command import *
from src.commands.extracts.refresh_extracts_command import *
from src.commands.group.create_group_command import *
from src.commands.group.delete_group_command import *
from src.commands.help.help_command import *
from src.commands.project.create_project_command import *
from src.commands.project.delete_project_command import *
from src.commands.project.publish_samples_command import *
from src.commands.site.create_site_command import *
from src.commands.site.delete_site_command import *
from src.commands.site.edit_site_command import *
from src.commands.site.list_sites_command import *
from src.commands.user.add_users_command import *
from src.commands.user.create_site_users import *
from src.commands.user.delete_site_users_command import *

# from src.commands.user.create_users import *
from src.commands.user.remove_users_command import *


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
        HelpCommand,
        ListSiteCommand,
        LoginCommand,
        LogoutCommand,
        PublishCommand,
        PublishSamplesCommand,
        ReencryptExtracts,
        RefreshExtracts,
        RemoveUserCommand,
    ]
