import argparse
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class HelpCommand:
    """
    Command to show user help options
    """

    name: str = "help"
    description = "Show message listing commands and global options, then exit"
    usage = (
        "tabcmd help             -- Show message listing commands and global options, then exit\n"
        "tabcmd <command>        -- Run a specific command {0}\n"
        "tabcmd <command> -h     -- Show Help for a specific command\n\n"
        "More help: https://tableau.github.io/tabcmd/\n\n"
    )


    @staticmethod
    def define_args(parser):
        parser.add_argument("help_option", nargs="?")

    @staticmethod
    def run_command(args: argparse.Namespace):
        # delayed import because cyclical - commands shouldn't generally reference the command structure
        from tabcmd.execution.map_of_commands import CommandsMap
        from tabcmd.execution.parent_parser import version
        logger = log(__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        all_commands = CommandsMap.commands_hash_map

        logger.info("tabcmd - Tableau Server Command Line Utility {0} \n".format(version))
        logger.info("Usage:\n")
        logger.info(HelpCommand.usage.format("(see list below)"))

        if args.help_option:
            # identify if the command was 'tabcmd help -h' - they just want instructions for running help
            if args.help_option == "-h":
                exit(0)

            logger.info(all_commands.a)
            cmd = list(all_commands).filter(lambda command: command.name == args.help_option, all_commands)
            if cmd is not None:
                from tabcmd.execution.parent_parser import ParentParser
                parser = ParentParser.get_command_args(cmd)
                logger.info(parser.print_help())


        else:
            logger.info("Tabcmd commands:\n")
            for cmd in all_commands:
                logger.info("\t" + cmd.name + ": " + cmd.description)
            logger.info("\nGlobal settings")

            from tabcmd.execution.parent_parser import parent_parser_with_global_options
            parser = parent_parser_with_global_options()
            logger.info(parser.print_help())
            logger.info(HelpCommand.usage.format(""))
