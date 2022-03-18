class HelpCommand:
    """
    Command to show user help options
    """

    name: str = "help"
    description: str = "Show Help and exit"

    @classmethod
    def parse(cls):
        pass

    @staticmethod
    def run_command(args):
        pass
