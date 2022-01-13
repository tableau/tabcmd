import argparse
import sys
import textwrap
from .help_parser import HelpParser

# class RawFormatter(argparse.HelpFormatter):
#     def _fill_text(self, text, width, indent):
#         return "\n".join([textwrap.fill(line, width) for line in
#                           textwrap.indent(textwrap.dedent(text), indent).splitlines()])


class ParentParser:
    """Parser that will be inherited by all commands. Contains
    authentication and logging level setting"""

    def parent_parser_with_global_options(self):
        parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, add_help=False)
        parser.add_argument('--server', '-s', metavar='',
                            help='server of account holder')
        parser.add_argument('--username', '-u', metavar='',
                            help='username of account holder')
        parser.add_argument('--site', '-t', default=None, metavar='',
                            help='Used in the URL to uniquely identify the '
                                 'site.')
        parser.add_argument('--password', '-p', metavar='',
                            help='password of account holder')
        prompt_group = parser.add_mutually_exclusive_group()
        prompt_group.add_argument('--no-prompt', action='store_true',
                                  help='no prompt for password')
        prompt_group.add_argument('--prompt', action='store_true',
                                  help='prompt for password')
        parser.add_argument('--logging-level', '-l',
                            choices=['debug', 'info', 'error'],
                            default='info',
                            help='desired logging level '
                                 '(set to error by default)')
        parser.add_argument('--token', '-to', default=None, metavar='',
                            help='personal access token to '
                                 'sign into the '
                                 'server')
        parser.add_argument('--token-name', '-tn', metavar='',
                            help='name of the personal access '
                                 'token used to sign into the server')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--no-cookie', action='store_true',
                           help='do not save session id')
        group.add_argument('--cookie', action='store_true',
                           help='save session id')
        return parser
