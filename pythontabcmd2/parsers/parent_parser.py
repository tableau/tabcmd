import argparse
from ..tabcmd2_controller import Tabcmd2Controller


class ParentParser:
    def parent_parser_with_global_options(self):

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--server', '-s',
                            help='server of account holder')
        parser.add_argument('--username', '-u',
                            help='username of account holder')
        parser.add_argument('--site', '-S', default=None,
                            help='site of account holder')
        parser.add_argument('--password', '-p',
                            help='username of account holder')
        parser.add_argument('--no-prompt', '-n', default=None,
                            help='no prompt for password')
        parser.add_argument('--logging-level', '-l',
                            choices=['debug', 'info', 'error'],
                            default='error',
                            help='desired logging level '
                                 '(set to error by default)')
        return parser

