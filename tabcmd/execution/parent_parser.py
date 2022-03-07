import argparse


class ParentParser:
    """Parser that will be inherited by all commands. Contains
    authentication and logging level setting"""

    def __init__(self):
        self.global_options = self.parent_parser_with_global_options()
        self.root = argparse.ArgumentParser(parents=[self.global_options])
        # https://stackoverflow.com/questions/7498595/python-argparse-add-argument-to-multiple-subparsers
        self.subparsers = self.root.add_subparsers()

    def get_root_parser(self):
        return self.root

    def include(self, command):
        additional_parser = self.subparsers.add_parser(command[0], help=command[2], parents=[self.global_options])
        # This line is where we actually set each parser to call the correct command
        additional_parser.set_defaults(func=command[1])
        return additional_parser

    # ordered alphabetically by short option - this is reflected directly in help output
    def parent_parser_with_global_options(self):
        parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, add_help=False)

        # The default behavior is to try certificates in the computer store, like a browser?
        # There is no option to say 'use defaults'
        certificates = parser.add_mutually_exclusive_group()
        certificates.add_argument(
            "-c",
            "--use-certificate",
            dest="certificate",
            metavar="",
            help="Use client certificate to sign in. Required when mutual SSL is enabled.",
        )
        certificates.add_argument(
            "--no-certcheck",
            action="store_true",
            help="When specified, tabcmd (the client) does not validate the server's SSL certificate.",
        )

        cookies = parser.add_mutually_exclusive_group()
        cookies.add_argument(
            "--cookie",
            action="store_true",
            help="Save the session ID when signing in. Subsequent commands will NOT need to sign in again. This is \
            the default behavior.",
        )
        cookies.add_argument(
            "--no-cookie",
            action="store_true",
            help="Do not save the session ID when signing in. Subsequent commands will need to sign in again.",
        )

        parser.add_argument(
            "-l",
            "--logging-level",
            choices=["DEBUG", "INFO", "ERROR"],
            default="info",
            metavar="",
            help="Use the specified logging level. If not specified, the default level is INFO.",
        )

        parser.add_argument("--no-prompt", action="store_true", help="no prompt for password")

        auth_options = parser.add_mutually_exclusive_group()
        auth_options.add_argument(
            "-tn",
            "--token-name",
            metavar="<TOKEN NAME>",
            help="The name of the Tableau Server Personal Access Token. If using a token to sign in,\
                  this is required at least once to begin session.",
        )
        auth_options.add_argument(
            "-u",
            "--username",
            metavar="<USER>",
            help="Use the specified Tableau Server username. For Tableau Online, this will be an email address.",
        )

        secret_values = parser.add_mutually_exclusive_group()
        secret_values.add_argument(
            "-to",
            "--token",
            default=None,
            metavar="<TOKEN VALUE>",
            help="Use the specified Tableau Server Personal Access Token. Requires --token-name to be set.",
        )
        secret_values.add_argument(
            "-p",
            "--password",
            metavar="<PASSWORD>",
            help="Use the specified Tableau Server password. Requires --username to be set.",
        )
        secret_values.add_argument(
            "--password-file",
            metavar="<FILE>",
            help="Read the password from the given .txt file rather than the command line for increased security.",
        )

        proxy_group = parser.add_mutually_exclusive_group()
        proxy_group.add_argument(
            "-x",
            "--proxy",
            dest="proxy",
            metavar="<HOST:PORT>",
            help="Connect to Tableau Server using the specified HTTP proxy.",
        )
        proxy_group.add_argument(
            "--no-proxy",
            action="store_false",
            dest="proxy",
            help="Do not use a HTTP proxy.",
        )  # is this the default behavior?

        parser.add_argument(
            "-s",
            "--server",
            default="http://localhost",
            metavar="<URL>",
            help="Use the specified Tableau Server URL. If no protocol is specified, http:// is assumed.",
        )
        parser.add_argument(
            "-t",
            "--site",
            default="",
            metavar="SITEID",
            help='Use the specified Tableau Server site. Leave empty or specify an empty string ("") to \
                    force use of the default site',
        )

        parser.add_argument(
            "--timeout",
            metavar="<SECONDS>",  # can't use -t, it's already used for --site
            help="How long to wait, in seconds, for the server to complete processing the command. The default \
                    behavior is to wait until the server responds.",
        )

        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version="%(prog)s (v2.pre-release)",
            help="Show version information and exit.",
        )

        return parser
