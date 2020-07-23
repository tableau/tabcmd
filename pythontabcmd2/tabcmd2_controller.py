try:
    from constants import Constants
    from commands.auth.login_command import *
    from commands.project.create_project_command import *
    from commands.project.delete_project_command import *
    from commands.group.create_group_command import *
    from commands.group.delete_group_command import *
    from commands.user.create_users_command import *
    from commands.user.remove_users_command import *
    from commands.user.delete_users_command import *
    from parsers.login_parser import *
    from parsers.create_project_parser import *
    from parsers.delete_project_parser import *
    from parsers.create_group_parser import *
    from parsers.delete_group_parser import *
    from parsers.create_users_parser import *
    from parsers.remove_users_parser import *
    from parsers.delete_users_parser import *
    from logger_config import get_logger
except ModuleNotFoundError:
    from . import tableauserverclient as TSC
    from .constants import Constants
    from commands.auth.login_command import *
    from commands.project.create_project_command import *
    from commands.project.delete_project_command import *
    from commands.group.create_group_command import *
    from commands.group.delete_group_command import *
    from commands.user.create_users_command import *
    from commands.user.remove_users_command import *
    from commands.user.delete_users_command import *
    from .parsers.login_parser import *
    from .parsers.create_project_parser import *
    from .parsers.delete_project_parser import *
    from .parsers.create_group_parser import *
    from .parsers.delete_group_parser import *
    from .parsers.create_users_parser import *
    from .parsers.remove_users_parser import *
    from .parsers.delete_users_parser import *
    from .logger_config import *

logger = get_logger('pythontabcmd2.tabcmd2_controller')


class Tabcmd2Controller:
    def __init__(self):
       pass

    def get_command_strategy(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('command', help='tabcmd commands to run')
        args = parser.parse_args(sys.argv[1:2])
        if args.command is None:
            logger.info('Unrecognized command please try again')
            parser.print_help()
        else:
            return args.command




