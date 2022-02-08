from .tabcmd_controller import *
from .context import *
import sys


def main():

    if sys.version_info < (3,6):
        raise ImportError("Tabcmd requires Python 3.6 but you are on Python 2.\
            Please update your python version.")

    tabcmd_controller = TabcmdController()
    command_strategy = tabcmd_controller.get_command_strategy()
    command_context = Context(command_strategy)
    command_context.execute_command()


if __name__ == "__main__":
    main()
