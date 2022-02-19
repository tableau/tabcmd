from .map_of_commands import *
from .map_of_parsers import *
from .parent_parser import ParentParser

"""
This is where we go through all the parsers and manually attach them to a command
"""


class TabcmdController:

    def initialize_parsers(self):
        manager = ParentParser()
        parent = manager.get_root_parser()

        commands = CommandsMap.commands_hash_map
        parsers = ParsersMap.parsers_hashmap
        for commandname in commands.keys():
            parsers[commandname](manager, commands[commandname])

        return parent
