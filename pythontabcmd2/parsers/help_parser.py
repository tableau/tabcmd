import sys
import argparse


class HelpParser:
    @classmethod
    def print_help_description(cls):
        description = \
            "Tabcmd2 - Tableau Server Command Line Utility 2.0 \n \n" \
            "tabcmd2 help             -- Help for tabcmd commands \n" \
            "tabcmd2 help <a command> -- Show Help for a specific command\n" \
            "tabcmd2 help commands    -- List all available commands\n\n"
        sys.stdout.write(description)

    @staticmethod
    def help_parser():
        parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, add_help=False)
        parser.add_argument('--server', '-s', metavar='',
                            help='server of account holder')