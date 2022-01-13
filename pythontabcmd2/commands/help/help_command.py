
from .. import Constants
import tableauserverclient as TSC
from .. import log
import os
from .. import LogoutParser
from ... import Session
from .. import HelpParser


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
        print("THESE ARE THE ARGS", self.args)
        print("HELLP WPRLD")
