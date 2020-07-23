import argparse
import sys
import argparse
from .logger_config import get_logger
# try:
#     from constants import Constants
#     from logger_config import get_logger
# except ModuleNotFoundError:
#     from . import tableauserverclient as TSC
#     from .constants import Constants
#     from .logger_config import *

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




