from .map_of_commands import CommandsMap
from .commands.auth.login_command import *
# from .commands.project.create_project_command import *
# from .commands.project.delete_project_command import *
# from .commands.group.delete_group_command import *
# from .commands.group.create_group_command import *
# from .commands.user.create_users_command import *
# from .commands.user.delete_users_command import *
# from .commands.user.remove_users_command import *
# from .commands.auth.logout_command import *

import sys


class Context:

    def __init__(self, command_strategy):
        self.command_strategy = command_strategy

    def execute_command(self):
        # command_strategy_type = eval(hash_map.get(self.command_strategy))
        command_strategy_type = getattr(sys.modules[__name__], CommandsMap.commands_hash_map.get(self.command_strategy))
        command_strategy = command_strategy_type.parse()
        command_strategy.run_command()
