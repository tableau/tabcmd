from .tabcmd2_controller import *
from .context import *


def main():
    tabcmd_controller = Tabcmd2Controller()
    command_strategy = tabcmd_controller.get_command_strategy()
    command_context = Context(command_strategy)    # TODO
    command_context.execute_command()
