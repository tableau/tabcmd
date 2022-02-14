from .map_of_commands import *
from .map_of_parsers import *

logger = get_logger('tabcmd.tabcmd_controller', 'info')


class TabcmdController:

    def get_command_strategy(self):
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        if len(sys.argv) > 2 and sys.argv[1] == "help" \
                and sys.argv[2] == "commands":
            HelpParser.print_help_description()
            TabcmdController.get_list_of_commands_available()
            parser.print_help()
            sys.exit()
        if len(sys.argv) > 2 and sys.argv[1] == "help" and sys.argv[2] is not \
                None:
            if sys.argv[2] in ParsersMap.parsers_hashmap:
                ParsersMap.parsers_hashmap[sys.argv[2]]()
            else:
                print("Please check the command entered and try again")
                sys.exit()
        parser.add_argument('command', nargs='?', default="help")
        args = parser.parse_args(sys.argv[1:2])
        if args.command is not None:
            return args.command
        elif len(sys.argv) == 1 or sys.argv[1]:
            HelpParser.print_help_description()
            parser.print_help()
            sys.exit()

    @classmethod
    def get_list_of_commands_available(cls):
        for command, command_tuple in CommandsMap.commands_hash_map.items():
            TabcmdController.print_formatted_list(command, command_tuple[1])

    @classmethod
    def print_formatted_list(cls, command, description_of_command):
        print(" %-20s %-15s %-5s" % (command, "--", description_of_command))
