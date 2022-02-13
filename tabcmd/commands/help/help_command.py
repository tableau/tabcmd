
from .. import log
from .. import HelpParser
from .. import ParentParser


class HelpCommand:
    """
    Command to show user help options
    """
    @classmethod
    def parse(cls):
        args = HelpParser.help_parser()
        return cls(args)

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        HelpParser.print_help_description()
        parser.print_help()
