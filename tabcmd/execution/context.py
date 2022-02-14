from .map_of_commands import CommandsMap
from tabcmd.commands.auth.login_command import *
from tabcmd.commands.project.create_project_command import *
from tabcmd.commands.project.delete_project_command import *
from tabcmd.commands.group.delete_group_command import *
from tabcmd.commands.group.create_group_command import *
from tabcmd.commands.user.remove_users_command import *
from tabcmd.commands.auth.logout_command import *
from tabcmd.commands.user.add_users_command import *
from tabcmd.commands.site.create_site_command import *
from tabcmd.commands.user.create_site_users import *
from tabcmd.commands.site.delete_site_command import *
from tabcmd.commands.site.delete_site_users_command import *
from tabcmd.commands.site.edit_site_command import *
from tabcmd.commands.site.list_sites_command import *
from tabcmd.commands.datasources_and_workbooks.delete_command import *
from tabcmd.commands.datasources_and_workbooks.export_command import *
from tabcmd.commands.datasources_and_workbooks.publish_command import *
from tabcmd.commands.datasources_and_workbooks.get_url_command import *
from tabcmd.commands.help.help_command import *
from tabcmd.commands.extracts.create_extracts_command import *
from tabcmd.commands.extracts.decrypt_extracts_command import *
from tabcmd.commands.extracts.delete_extracts_command import *
from tabcmd.commands.extracts.refresh_extracts_command import *
from tabcmd.commands.extracts.reencrypt_extracts_command import *
from tabcmd.commands.extracts.encrypt_extracts_command import *
import sys


class Context:

    def __init__(self, command_strategy):
        self.command_strategy = command_strategy

    def execute_command(self):
        command_strategy_type = getattr(sys.modules[__name__],
                                        CommandsMap.commands_hash_map.
                                        get(self.command_strategy)[0])
        args = command_strategy_type.parse()
        command_strategy_type.run_command(args)
