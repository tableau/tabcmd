import logging
import sys

from .localize import set_client_locale
from .logger_config import log
from .parent_parser import ParentParser

from tabcmd.version import version


class TabcmdController:
    @staticmethod
    def initialize():
        manager = ParentParser()
        parent = manager.connect_commands()
        manager.include_help()
        return parent

    # during normal execution, leaving input as none will default to sys.argv
    # for testing, we want to be able to pass in different updates
    @staticmethod
    def run(parser, user_input=None):
        if user_input is None and len(sys.argv) <= 1:  # no arguments given
            parser.print_help()
            sys.exit(0)
        user_input = user_input or sys.argv[1:]
        namespace = parser.parse_args(user_input)
        if hasattr("namespace", "logging_level") and namespace.logging_level != logging.INFO:
            print("logging:", namespace.logging_level)

        logger = log(__name__, namespace.logging_level or logging.INFO)
        logger.info("Tabcmd {}".format(version))
        if (hasattr("namespace", "password") or hasattr("namespace", "token_value")) and hasattr("namespace", "func"):
            # don't print whole namespace because it has secrets
            logger.debug(namespace.func)
        else:
            logger.debug(namespace)
        if namespace.language:
            set_client_locale(namespace.language, logger)
        try:
            func = namespace.func
            # if a subcommand was identified, call the function assigned to it
            # this is the functional equivalent of the call by reflection in the previous structure
            # https://stackoverflow.com/questions/49038616/argparse-subparsers-with-functions
            namespace.func.run_command(namespace)
        except AttributeError:
            parser.error("No command identified or too few arguments")
        except Exception as e:
            # todo: use log_stack here for better presentation?
            logger.exception(e)
            # if no command was given, argparse will just not create the attribute
            sys.exit(2)

        return namespace
