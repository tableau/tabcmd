import sys

from .map_of_commands import *
from .parent_parser import ParentParser
from .localize import set_client_locale


class TabcmdController:
    @staticmethod
    def initialize():
        manager = ParentParser()
        parent = manager.get_root_parser()

        commands = CommandsMap.commands_hash_map
        for command in commands:
            manager.include(command)
        return parent

    # during normal execution, leaving input as none will default to sys.argv
    # for testing, we want to be able to pass in different updates
    @staticmethod
    def run(parser, user_input=None):
        if user_input is None and len(sys.argv) <= 1:  # no arguments given
            parser.print_help()
            sys.exit(0)
        user_input = user_input or sys.argv[1:]
        namespace = parser.parse_args(user_input)

        if namespace.language:
            set_client_locale(namespace.language)

        try:
            command_name = namespace.func
        except AttributeError as aer:
            parser.print_help()
            sys.exit(2)

        if not command_name:
            parser.print_help()
            sys.exit(0)

        # if a subcommand was identified, call the function assigned to it
        # this is the functional equivalent of the call by reflection in the previous structure
        # https://stackoverflow.com/questions/49038616/argparse-subparsers-with-functions
        namespace.func.run_command(namespace)
        return namespace
