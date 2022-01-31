import sys
import argparse


class HelpParser:
    @classmethod
    def print_help_description(cls):
        description = \
            "tabcmd - Tableau Server Command Line Utility 2.0 \n \n" \
            "tabcmd help             -- Help for tabcmd commands \n" \
            "tabcmd help <a command> -- Show Help for a specific command\n" \
            "tabcmd help commands    -- List all available commands\n\n"
        sys.stdout.write(description)

    @staticmethod
    def help_parser():
        pass
