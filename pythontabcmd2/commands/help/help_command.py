
from .. import Constants
import tableauserverclient as TSC
from .. import log
import os
from .. import LogoutParser
from ... import Session
from .. import HelpParser
from .. import ParentParser


class HelpCommand:
    """
    Command to show user help options
    """
    def __init__(self, args):
        self.args = args

    @classmethod
    def parse(cls):
        args = HelpParser.help_parser()
        return cls(args)

    def run_command(self):
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        HelpParser.print_help_description()
        parser.print_help()
        print("THESE ARE THE ARGS", self.args)
        print("HELLP WPRLD")
