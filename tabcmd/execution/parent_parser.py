import argparse

from .localize import _
from .logger_config import log
from .map_of_commands import CommandsMap
from tabcmd.version import version

"""
Note: output order is influenced first by grouping, then by order they are added in here
Most of this function is about making the help output look nice.
Argparse uses argument groups to separate arguments in the help output - but that doesn't
work quite as documented when in nested parsers, like we have.
Everything that is just added directly to the parser will be in the default set of 
'optional arguments' directly on the newly created parser, which is renamed 'behavior arguments' to
differentiate from the signin/connection options.
Everything we add to a mutually-exclusive-group in here will be in the default set of
'optional arguments' on the *parent* parser, which is displayed all together. To make this a nice set,
many arguments are added to a mutually-exclusive-group of one argument. They are named things like
'formatting_group1' to make it clear this is a formatting choice, not functional.
The arguments for each command must be added to a group for that command.
"""


def parent_parser_with_global_options():
    parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, add_help=False)
    parser._optionals.title = _("tabcmdparser.global.behaviors")

    formatting_group1 = parser.add_mutually_exclusive_group()
    formatting_group1.add_argument(
        "-s",
        "--server",
        default=None,  # default is handled in Session class
        metavar="<URL>",
        help=_("session.options.server"),
    )

    formatting_group2 = parser.add_mutually_exclusive_group()
    formatting_group2.add_argument("-t", "--site", default="", dest="site_name", metavar="SITEID", help=_("session.options.site"))

    auth_options = parser.add_mutually_exclusive_group()
    auth_options.add_argument("--token-name", default=None, metavar="<TOKEN NAME>", help=_("tabcmd.options.token_name"))
    auth_options.add_argument("-u", "--username", default=None, metavar="<USER>", help=_("session.options.username"))

    secret_values = parser.add_mutually_exclusive_group()
    secret_values.add_argument("--token-value", default=None, metavar="<TOKEN VALUE>", help=_("tabcmd.options.token_value"))
    secret_values.add_argument("-p", "--password", default=None, metavar="<PASSWORD>", help=_("session.options.password"))
    secret_values.add_argument("--password-file", default=None, metavar="<FILE>", help=_("session.options.password-file"))
    secret_values.add_argument("--token-file", default=None, metavar="<FILE>", help=_("tabcmd.options.token_file"))

    formatting_group3 = parser.add_mutually_exclusive_group()
    formatting_group3.add_argument("--no-prompt", action="store_true", help=_("session.options.no-prompt"))

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

    formatting_group4 = parser.add_mutually_exclusive_group()
    formatting_group4.add_argument("--no-cookie", action="store_true", help=_("session.options.no-cookie"))

    proxy_group = parser.add_mutually_exclusive_group()
    proxy_group.add_argument(
        "-x", "--proxy", dest="proxy", default=None, metavar="<HOST:PORT>", help=_("session.options.proxy")
    )
    proxy_group.add_argument(
        "--no-proxy",
        action="store_true",  # default to false
        help=_("session.options.no-proxy"),
    )

    formatting_group5 = parser.add_mutually_exclusive_group()
    formatting_group5.add_argument(
        "--timeout",
        default=None,  # default is handled in Session class
        metavar="<SECONDS>",  # can't use -t, it's already used for --site
        help=_("session.options.timeout"),
    )

    # general behavioral options
    parser.add_argument(
        "--continue-if-exists",
        action="store_true",  # default behavior matches old tabcmd
        help=_("tabcmd.options.conflicts"),  # kind of equivalent to 'overwrite' in the publish command
    )

    parser.add_argument(
        "--country",
        choices=["de", "en", "es", "fr", "it", "ja", "ko", "pt", "sv", "zh"],
        type=str.lower,  # coerce input to lowercase to act case insensitive
        help=_("export.options.country"),
    )

    parser.add_argument(
        "--language",
        choices=["de", "en", "es", "fr", "it", "ja", "ko", "pt", "sv", "zh"],
        type=str.lower,  # coerce input to lowercase to act case insensitive
        help=_("tabcmd.options.language.detailed"),
    )

    parser.add_argument(
        "-l",
        "--logging-level",
        choices=["TRACE", "DEBUG", "INFO", "ERROR"],
        type=str.upper,  # coerce input to uppercase to act case insensitive
        default="info",
        help=_("tabcmd.options.log"),
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=_("tabcmd.name") + "v" + version + "\n \n",
        help=_("version.description"),
    )
    return parser


class ParentParser:
    # Ref https://docs.python.org/3/library/argparse.html
    """Parser that will be inherited by all commands. Contains authentication and logging level setting"""

    def __init__(self):
        self.global_options = parent_parser_with_global_options()
        self.root = argparse.ArgumentParser(
            prog="tabcmd", 
            description="tabcmd <command>      -- " + _("tabcmd.howto"),
            parents=[self.global_options], 
            epilog=_("tabcmdparser.link.help")
        )
        self.root._optionals.title =  _("tabcmdparser.global.connections")
        # https://stackoverflow.com/questions/7498595/python-argparse-add-argument-to-multiple-subparsers
        self.subparsers = self.root.add_subparsers(
            title=_("tabcmdparser.help.commands"),
            description=_("tabcmdparser.help.specific"),
            metavar="{<command> [command args]}",  # instead of printing the list of choices
        )

    def get_root_parser(self):
        return self.root

    def connect_commands(self):
        commands = CommandsMap.commands_hash_map
        for command in commands:
            self.include(command)
        return self.root

    def include(self, command):
        additional_parser = self.subparsers.add_parser(
            command.name, help=command.description, parents=[self.global_options]
        )
        additional_parser._optionals.title =  _("tabcmdparser.global.connections")
        # This line is where we actually set each parser to call the correct command
        additional_parser.set_defaults(func=command)
        command.define_args(additional_parser)
        return additional_parser

    def include_help(self):
        additional_parser = self.subparsers.add_parser("help", help=_("tabcmdparser.help.description") , parents=[self.global_options])
        additional_parser._optionals.title =  _("tabcmdparser.global.connections")
        additional_parser.set_defaults(func=Help(self))


class Help:

    parser = None
    # This needs to have access to the parser when it gets called
    def __init__(self, _parser: ParentParser):
        self.parser = _parser

    def run_command(self, args):
        logger = log(__name__, "info")
        logger.info(_("tabcmd.name") + " " + version + "\n")
        logger.info(self.parser.root.format_help())

