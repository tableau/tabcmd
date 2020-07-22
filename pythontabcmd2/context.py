from map_of_commands import *
import sys
class Context:

    def __init__(self, command_strategy):
        self.command_strategy = command_strategy

    def execute_command(self):
       # command_strategy_type = eval(hash_map.get(self.command_strategy))
        command_strategy_type = getattr(sys.modules[__name__],CommandsMap.commands_hash_map.get(self.command_strategy))
        command_strategy = command_strategy_type.parse()
        command_strategy.run_command()