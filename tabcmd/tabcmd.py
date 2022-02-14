from .tabcmd_controller import *
from .context import *
import sys


def main():

    if sys.version_info < (3, 7):
        raise ImportError("Tabcmd requires Python 3.7 but you are on " +
                          sys.version_info +
                          " - please update your python version.")

    tabcmd_controller = TabcmdController()
    command_strategy = tabcmd_controller.get_command_strategy()
    command_context = Context(command_strategy)
    command_context.execute_command()


if __name__ == "__main__":
    main()
