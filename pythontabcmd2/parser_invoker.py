import argparse
import sys
from shlex import split
import getpass
import dill as pickle
import os
from os import path, remove
import logging
try:
    import tableauserverclient as TSC  
    from constants_errors import Constants
    from session import *
    from commands.create_project import *
    from parsers.login_parser import *
    from parsers.create_project_parser import *
    from logger_config import get_logger
except:
    from . import tableauserverclient as TSC
    from .constants_errors import Constants
    from .session import *
    from .commands.create_project import *
    from .parsers.login_parser import *
    from .parsers.create_project_parser import *
    from .logger_config import get_logger
    

logger = get_logger('pythontabcmd2.parser_invoker')

class ParserInvoker(Constants):  
    def __init__(self):
        """Initializes a parser through Argparse module"""
        parser = argparse.ArgumentParser()
        parser.add_argument('command', help='tabcmd commands to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            logger.info('Unrecognized command please try again')
            parser.print_help()
        getattr(self, args.command)()  # Invoke method with the same name

    def login(self):
        """ Method to parse login details of user"""
        login_parser = LoginParser()
        username, password, site, server, token_name, personal_access_token = login_parser.login_parser()
        session = Session(server, username, password, token_name, site, personal_access_token)
        session.create_session()
        
    def createproject(self):
        """ Method that will be called when user enters create project on the command line"""
        create_project_parser_obj = CreateProjectParser()
        name, description, content_perm, parent_proj_path = create_project_parser_obj.create_project_parser()
        signed_in_object, server_object = self.deserialize()
        try:
            create_new_project = CreateProject(name, description, content_perm, parent_proj_path)
            create_new_project.create_project(server_object)
        except TSC.ServerResponseError as e:
            if e.code == Constants.invalid_credentials:
                logger.info("Authentication Error, Please login again") 

    def deserialize(self):
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
        
    def logout(self):
        """ Method to log out from the current session """
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, 'tabcmd.pkl')
        signed_in_object, server_object = self.deserialize()
        server_object.auth.sign_out()
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info("Logged out successfully")
        else:
            logger.info("Not logged in")


        






