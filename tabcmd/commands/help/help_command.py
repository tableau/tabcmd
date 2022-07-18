import argparse
from typing import Any, List

from src.execution.localize import _
from src.execution.logger_config import log


class HelpCommand:
    """
    Command to show user help options
    """

    name: str = "help"
    description: str = "Show Help and exit"

    @staticmethod
    def define_args(parser):
        parser.add_argument("help_option", nargs="?")

    @staticmethod
    def run_command(args: argparse.Namespace):

        # whaddya mean, '__class__' is not defined ??!?!!?
        logger = log(__class__.__name__, args.logging_level)  # type: ignore[name-defined]
        logger.debug(_("tabcmd.launching"))

        # delayed import, TODO fix cyclic imports
        from src.execution.map_of_commands import CommandsMap

        all_commands: List[Any] = CommandsMap.commands_hash_map

        description: str = (
            "tabcmd - Tableau Server Command Line Utility 2.0 \n \n"
            "tabcmd help             -- List all available commands and global options \n"
            "tabcmd help <a command> -- Show Help for a specific command\n\n"
        )

        if args.help_option:

            if args.help_option in map(lambda command: command.name, all_commands):
                command_objects = filter(lambda command: command.name == args.help_option, all_commands)
                cli_cmd = list(command_objects)[0]
                logger.info(cli_cmd.name.ljust(25) + cli_cmd.description + "\n")
                command_parser = argparse.ArgumentParser(parents=[])
                cli_cmd.define_args(command_parser)

                positionals = []
                optionals = []
                for option in command_parser._actions:
                    if option.option_strings:
                        optionals.append(option)
                    else:
                        positionals.append(option)

                if positionals:
                    logger.info("Required arguments")
                for option in positionals:
                    logger.info("{0} {1}{2}{3}".format(option.dest.ljust(25), "{", option.help, "}"))
                if optionals:
                    logger.info("\nOptional arguments")
                for option in optionals:
                    logger.info("{0} {1} ".format(option.option_strings, option.help))

                logger.info("\nUsage")
                usage = cli_cmd.name + " "
                for opt in positionals:
                    usage = usage + opt.dest
                if len(positionals) < len(command_parser._actions):
                    usage = usage + "  [--optional arguments]"
                logger.info(usage)

        else:
            for cmd in all_commands:
                logger.info(cmd.name + ": " + cmd.description)
