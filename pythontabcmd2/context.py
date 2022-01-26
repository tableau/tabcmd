from .map_of_commands import CommandsMap
from .commands.auth.login_command import *
from .commands.project.create_project_command import *
from .commands.project.delete_project_command import *
from .commands.group.delete_group_command import *
from .commands.group.create_group_command import *
from .commands.user.remove_users_command import *
from .commands.auth.logout_command import *
from .commands.user.add_users_command import *
from .commands.site.create_site_command import *
from .commands.user.create_site_users import *
from .commands.site.delete_site_command import *
from .commands.site.delete_site_users_command import *
from .commands.site.edit_site_command import *
from .commands.site.list_sites_command import *
from .commands.datasources_and_workbooks.delete_command import *
from .commands.datasources_and_workbooks.export_command import *
from .commands.datasources_and_workbooks.publish_command import *
from .commands.datasources_and_workbooks.get_url_command import *
from .commands.help.help_command import *
import sys


class Context:

    def __init__(self, command_strategy):
        self.command_strategy = command_strategy

    def execute_command(self):
        command_strategy_type = getattr(sys.modules[__name__],
                                        CommandsMap.commands_hash_map.
                                        get(self.command_strategy)[0])
        command_strategy = command_strategy_type.parse()
        command_strategy.run_command()
