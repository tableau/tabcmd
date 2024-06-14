import logging
import os
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
        # if no subcommand was given, call help
        if not hasattr(namespace, "func"):
            print("No command found.")
            parser.print_help()
            sys.exit(0)

        if hasattr("namespace", "logging_level") and namespace.logging_level != logging.INFO:
            print("logging:", namespace.logging_level)

        logger = log(__name__, namespace.logging_level or logging.INFO)
        logger.info("Tabcmd {}".format(version))
        if hasattr(namespace, "password") or hasattr(namespace, "token_value"):
            # don't print whole namespace because it has secrets
            logger.debug(namespace.func)
        else:
            logger.debug(namespace)
        if hasattr(namespace, "language"):
            set_client_locale(namespace.language, logger)
        if namespace.query_page_size:
            os.environ["TSC_PAGE_SIZE"] = str(namespace.query_page_size)
        try:
            # https://stackoverflow.com/questions/49038616/argparse-subparsers-with-functions
            namespace.func.run_command(namespace)
        except Exception as e:
            # todo: use log_stack here for better presentation?
            logger.exception(e)
            sys.exit(2)

        return namespace
