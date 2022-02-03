import argparse
import sys
import textwrap
from .help_parser import HelpParser


class ParentParser:
    """Parser that will be inherited by all commands. Contains
    authentication and logging level setting"""

    def parent_parser_with_global_options(self):
        parser = argparse.ArgumentParser(usage=argparse.SUPPRESS,
                                         add_help=False)
        parser.add_argument('--server', '-s', metavar='',
               help='Use the specified Tableau Server URL. If no protocol is specified, http:// is assumed')

        credential_group = parser.add_mutually_exclusive_group()
        credential_group.add_argument('--username', '-u', metavar='',
               help='The Tableau Server username. If using a password to sign in, this is required\
                     at least once to begin session.')
        credential_group.add_argument('--token-name', '-tn', metavar='',
               help='The name of the Tableau Server Personal Access Token. If using a token to sign in,\
                     this is required at least once to begin session.')

        password_group = parser.add_mutually_exclusive_group()
        password_group.add_argument('--password-file',
               help='Allows the password to be stored in the given .txt file rather than the command \
                    line for increased security.') # TODO: not yet implemented? Should it work for a token too?
        password_group.add_argument('--password', '-p', metavar='',
                            help='The Tableau Server password, which is required at least once to begin session.')
        password_group.add_argument('--token', '-to', default=None, metavar='',
                            help='personal access token to sign into the server')

        parser.add_argument('--site', '-t', default='', metavar='',
               help='Use the specified Tableau Server site. Specify an empty string ("") to force use of\
                                 the default site')

        prompt_group = parser.add_mutually_exclusive_group()
        # the variable args.prompt will be set to false if --no-prompt is present
        prompt_group.add_argument('--no-prompt', action='store_false', dest='prompt',
                                  help='no prompt for password')
        prompt_group.add_argument('--prompt', action='store_true', dest='prompt',
                                  help='prompt for password')

        parser.add_argument('--logging-level', '-l',
                            choices=['debug', 'info', 'error'],
                            default='info',
                            help='desired logging level (set to info by default)')

        group = parser.add_mutually_exclusive_group()
        # the variable args.no_cookie will be set to true if --no-cookie is present, false for --cookie
        group.add_argument('--no-cookie', action='store_true', dest='no_cookie',
                           help='Do not save the session ID when signing in. Subsequent commands will need \
                                to sign in again.')
        group.add_argument('--cookie', action='store_false', dest='no_cookie',
                           help='Save the session ID when signing in. Subsequent commands will not need to \
                                sign in again. If unspecified, this is the default behavior')

        parser.add_argument('--no-certcheck', action='store_true',
               help='When specified, tabcmd (the client) does not validate the server\'s SSL certificate.')

        proxy_group = parser.add_mutually_exclusive_group()
        proxy_group.add_argument('--no-proxy', action='store_false', dest='proxy',
               help='When specified, an HTTP proxy will not be used.')
        proxy_group.add_argument('--proxy', '-x', dest='proxy', metavar='Host:Port',
               help='Connect to Tableau Server using the specified HTTP proxy.')

        parser.add_argument('--use-certificate', '-c',
               help='Use client certificate to sign in. Required when mutual SSL is enabled.')
        parser.add_argument('--timeout', # can't use -t, is already used for --site
               help='Waits the specified number of seconds for the server to complete processing the \
                    command. By default, the process will wait until the server responds.')

        parser.add_argument('--version', '-v', action='version', version="%(prog)s (v2.pre-release)")

        return parser
