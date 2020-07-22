try:
    from .tabcmd2_controller import *
    from .context import *
except ModuleNotFoundError:
    from tabcmd2_controller import *
    from context import *




class Tabcmd:
    def main(self):
        tabcmd_controller = Tabcmd2Controller()
        command_strategy = tabcmd_controller.get_command_strategy()
        command_context = Context(command_strategy)    # TODO
        command_context.execute_command()


if __name__ == '__main__':
    main_object = Tabcmd()
    main_object.main()
