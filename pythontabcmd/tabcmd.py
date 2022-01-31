from .tabcmd_controller import *
from .context import *


def main():
    tabcmd_controller = tabcmdController()
    command_strategy = tabcmd_controller.get_command_strategy()
    command_context = Context(command_strategy)
    command_context.execute_command()


if __name__ == "__main__":
    main()
