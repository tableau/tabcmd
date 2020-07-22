from .command_strategy_interface import CommandStrategyInterface
import os
import sys
import dill as pickle
from logger_config import *

logger = get_logger('pythontabcmd2.commands')


class Commands(CommandStrategyInterface):
    @staticmethod
    def deserialize():
        """" Method to convert the pickle file back to an object """
        try:
            home_path = os.path.expanduser("~")
            file_path = os.path.join(home_path, 'tabcmd.pkl')
            with open(str(file_path), 'rb') as input:
                signed_in_object = pickle.load(input)
                server_object = pickle.load(input)
                return signed_in_object, server_object
        except IOError:
            logger.info("****** Please login first ******")
            sys.exit()
