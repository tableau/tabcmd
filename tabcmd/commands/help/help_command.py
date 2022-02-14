
from tabcmd.execution.logger_config import log
from tabcmd.parsers.help_parser import HelpParser
from tabcmd.execution.parent_parser import ParentParser


class HelpCommand:
    """
    Command to show user help options
    """
    @classmethod
    def parse(cls):
        args = HelpParser.help_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        HelpParser.print_help_description()
        parser.print_help()
