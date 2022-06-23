import argparse
from .localize import _

# when we drop python 3.8, this could be replaced with this lighter weight option
# from importlib.metadata import version, PackageNotFoundError
from pkg_resources import get_distribution, DistributionNotFound

try:
    version = get_distribution("tabcmd").version
except DistributionNotFound:
    version = "2.x.unknown"
    pass


class ParentParser:
    # Ref https://docs.python.org/3/library/argparse.html
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
        additional_parser = self.subparsers.add_parser(
            command.name, help=command.description, parents=[self.global_options]
        )
        # This line is where we actually set each parser to call the correct command
        additional_parser.set_defaults(func=command)
        command.define_args(additional_parser)
        return additional_parser

    # ordered alphabetically by short option - this is reflected directly in help output
    def parent_parser_with_global_options(self):
        parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, add_help=False)

        certificates = parser.add_mutually_exclusive_group()
        certificates.add_argument(
            "-c",
            "--use-certificate",
            dest="certificate",
            default=None,
            metavar="",
            help=_("session.options.use-certificate"),
        )
        certificates.add_argument(
            "--no-certcheck",
            action="store_true",
            help=_("session.options.no-certcheck"),
        )

        parser.add_argument(
            "--continue-if-exists",
            action="store_false",
            help="Treat resource conflicts as item creation success e.g project already exists",
        )

        parser.add_argument("--no-cookie", action="store_true", help=_("session.options.no-cookie"))

        parser.add_argument(
            "-l",
            "--logging-level",
            choices=["DEBUG", "INFO", "ERROR"],
            type=str.upper,  # coerce input to uppercase to act case insensitive
            default="info",
            help="Use the specified logging level. The default level is INFO.",
        )

        parser.add_argument("--no-prompt", action="store_true", help=_("session.options.no-prompt"))

        auth_options = parser.add_mutually_exclusive_group()
        auth_options.add_argument(
            "--token-name",
            default=None,
            metavar="<TOKEN NAME>",
            help="The name of the Tableau Server Personal Access Token. If using a token to sign in,\
                  this is required at least once to begin session.",
        )
        auth_options.add_argument(
            "-u", "--username", default=None, metavar="<USER>", help=_("session.options.username")
        )

        secret_values = parser.add_mutually_exclusive_group()
        secret_values.add_argument(
            "--token-value",
            default=None,
            metavar="<TOKEN VALUE>",
            help="Use the specified Tableau Server Personal Access Token. Requires --token-name to be set.",
        )
        secret_values.add_argument(
            "-p", "--password", default=None, metavar="<PASSWORD>", help=_("session.options.password")
        )
        secret_values.add_argument(
            "--password-file", default=None, metavar="<FILE>", help=_("session.options.password-file")
        )

        proxy_group = parser.add_mutually_exclusive_group()
        proxy_group.add_argument(
            "-x", "--proxy", dest="proxy", default=None, metavar="<HOST:PORT>", help=_("session.options.proxy")
        )
        proxy_group.add_argument(
            "--no-proxy",
            action="store_false",
            help=_("session.options.no-proxy"),
        )

        parser.add_argument(
            "-s",
            "--server",
            default=None,  # default is handled in Session class
            metavar="<URL>",
            help=_("session.options.server"),
        )
        parser.add_argument(
            "-t", "--site", default="", dest="site_name", metavar="SITEID", help=_("session.options.site")
        )

        parser.add_argument(
            "--timeout",
            default=None,  # default is handled in Session class
            metavar="<SECONDS>",  # can't use -t, it's already used for --site
            help=_("session.options.timeout"),
        )

        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version="Tableau Server Command Line Utility v" + version + "\n \n",
            help="Show version information and exit.",
        )

        # TODO get the list of choices dynamically?
        parser.add_argument(
            "--language",
            choices=["de", "en", "es", "fr", "it", "ja", "ko", "pt", "sv", "zh"],
            help="Set the language to use. Exported data will be returned in this lang/locale."
            "If not set, the client will use your computer locale, and the server will use your user account locale",
        )

        parser.add_argument(
            "--country",
            choices=["de", "en", "es", "fr", "it", "ja", "ko", "pt", "sv", "zh"],
            help=_("export.options.country"),
        )
        return parser
