import sys


class HelpCommand:
    """
    Command to show user help options
    """

    name: str = "help"
    description: str = "Show Help and exit"

    @staticmethod
    def define_args(parser):
        # takes no args
        pass

    @staticmethod
    def run_command(args):
        description = (
            "tabcmd - Tableau Server Command Line Utility 2.0 \n \n"
            "tabcmd help             -- Help for tabcmd commands \n"
            "tabcmd help <a command> -- Show Help for a specific command\n"
            "tabcmd help commands    -- List all available commands\n\n"
        )
        sys.stdout.write(description)
