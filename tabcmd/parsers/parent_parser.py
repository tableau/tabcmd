import argparse
import sys
import textwrap
from .help_parser import HelpParser


class ParentParser:
    """Parser that will be inherited by all commands. Contains
    authentication and logging level setting"""

     # ordered alphabetically by short option - this is reflected directly in help output
    def parent_parser_with_global_options(self):
        parser = argparse.ArgumentParser(usage=argparse.SUPPRESS,
                                         add_help=False)

        # The default behavior is to try certificates in the computer store, like a browser?
        # There is no option to say 'use defaults'
        # NOT YET IMPLEMENTED
        parser.add_argument('-c', '--use-certificate', metavar='',
               help='Use client certificate to sign in. Required when mutual SSL is enabled.')
        # NOT YET IMPLEMENTED
        parser.add_argument('-h', '--help', metavar='', help="Display tabcmd help and exit.")
        parser.add_argument('-l', '--logging-level', choices=['DEBUG', 'INFO', 'ERROR'], default='info', metavar='',
               help='Use the specified logging level. If not specified, the default level is INFO.')

        parser.add_argument('--no-certcheck', action='store_true',
               help='When specified, tabcmd (the client) does not validate the server\'s SSL certificate.')

        parser.add_argument('--no-prompt', action='store_true', help='no prompt for password')

        cookies = parser.add_mutually_exclusive_group()
        cookies.add_argument('--no-cookie', action='store_true',
               help='Do not save the session ID when signing in. Subsequent commands will need to sign in again.')
        cookies.add_argument('-o', '--cookie', action='store_true',
               help='Save the session ID when signing in. Subsequent commands will NOT need \
                                to sign in again. This is the default behavior.')

        auth_options = parser.add_mutually_exclusive_group()
        auth_options.add_argument('-n', '--token-name', metavar='<TOKEN NAME>',
               help='The name of the Tableau Server Personal Access Token. If using a token to sign in,\
                     this is required at least once to begin session.')
        parser.add_argument('-k', '--token', default=None, metavar='<TOKEN VALUE>',
               help='Use the specified Tableau Server Personal Access Token. Requires --token-name to be set.')
        parser.add_argument('-p', '--password', metavar='<PASSWORD>',
               help='Use the specified Tableau Server password. Requires --username to be set.')

        # NOT YET IMPLEMENTED
        parser.add_argument('--password-file', metavar='<FILE>',
               help='Allows the password to be stored in the given .txt file rather than the command \
                    line for increased security.') # TODO: not yet implemented? Should it work for a token too?

        # NOT YET IMPLEMENTED
        proxy_group = parser.add_mutually_exclusive_group()
        proxy_group.add_argument('--proxy', dest='proxy', metavar='<HOST:PORT>',
               help='Connect to Tableau Server using the specified HTTP proxy.')
        proxy_group.add_argument('--no-proxy', action='store_false', dest='proxy',
               help='Do not use a HTTP proxy.') # is this the default behavior?

        parser.add_argument('-s', '--server', metavar='<URL>',
               help='Use the specified Tableau Server URL. If no protocol is specified, http:// is assumed.')
        parser.add_argument('-t', '--site', default='', metavar='SITEID',
               help='Use the specified Tableau Server site. Leave empty or specify an empty string ("") to \
                    force use of the default site')

        # NOT YET IMPLEMENTED
        parser.add_argument('--timeout', metavar='<SECONDS>', # can't use -t, it's already used for --site
               help='How long to wait, in seconds, for the server to complete processing the command. The default \
                    behavior is to wait until the server responds.')

        auth_options.add_argument('-u', '--username', metavar='<USER>',
                help='Use the specified Tableau Server username. For Tableau Online, this will be an email address.')

        parser.add_argument('-v', '--version', action='version', version="%(prog)s (v2.pre-release)",
               help='Show version information and exit.')


        return parser
