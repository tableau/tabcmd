import argparse
import sys
from .parsers.parent_parser import ParentParser
from .logger_config import get_logger
from .parsers.help_parser import HelpParser


logger = get_logger('pythontabcmd2.tabcmd2_controller', 'info')


class Tabcmd2Controller:

    def get_command_strategy(self):
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        print(sys.argv)
        if len(sys.argv) == 1:
            HelpParser.print_help_description()
            parser.print_help()
        parser.add_argument('command', nargs='?', default="help")
        args = parser.parse_args(sys.argv[1:2])
        if args.command is not None:
            return args.command
