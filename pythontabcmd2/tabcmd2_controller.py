try:
    from constants import Constants
    from commands.auth.session import *
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
    from parsers.create_user_parser import *
    from parsers.remove_users_parser import *
    from parsers.delete_users_parser import *
    from logger_config import get_logger
except ModuleNotFoundError:
    from . import tableauserverclient as TSC
    from .constants import Constants
    from commands.auth.session import *
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
    from .parsers.create_user_parser import *
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


    # def login(self):
    #     """ Method to parse login details of user"""
    #     login_parser = LoginParser()
    #     username, password, site, server, token_name, personal_access_token = login_parser.login_parser()
    #     session = Session(server, username, password, token_name, site, personal_access_token)
    #     session.create_session()
        
    def createproject(self):
        """ Method that will be called when user enters create project on the command line"""
        create_project_parser_obj = CreateProjectParser
        name, description, content_perm, parent_proj_path = create_project_parser_obj.create_project_parser()
        signed_in_object, server_object = self.deserialize()
        try:
            create_new_project = CreateProjectCommand(name, description, content_perm, parent_proj_path)
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

    def deleteproject(self):
        """ Method to delete a user specified project """
        delete_project_parser_object = DeleteProjectParser()
        name, parent_proj_path = delete_project_parser_object.delete_project_parser()
        signed_in_object, server_object = self.deserialize()
        try:
            delete_user_passed_project = DeleteProjectCommand(name, parent_proj_path)
            delete_user_passed_project.delete_project(server_object)
        except TSC.ServerResponseError as e:
            logger.info("Error deleting check project name")

    def creategroup(self):
        """ Method to create a user specified group """
        create_group_parser_object = CreateGroupParser()
        name = create_group_parser_object.create_group_parser()
        signed_in_object, server_object = self.deserialize()
        try:
            create_group_obj = CreateGroupCommand(name)
            create_group_obj.create_group(server_object)
        except TSC.ServerResponseError as e:
            logger.info("Error creating group check group name")


    def deletegroup(self):
        """ Method to delete a user specified group """
        delete_group_parser_object = DeleteGroupParser()
        name = delete_group_parser_object.delete_group_parser()
        signed_in_object, server_object = self.deserialize()
        try:
            delete_user_passed_group = DeleteGroupCommand(name)
            delete_user_passed_group.delete_group(server_object)
        except TSC.ServerResponseError as e:
            logger.info("Error deleting check group name")

    def createusers(self):
        """ Method to create user on the server"""
        create_user_parser_object = CreateUserParser()
        lines_of_csv = create_user_parser_object.create_user_parser()
        create_user_command_obj = CreateUserCommand()
        signed_in_object, server_object = self.deserialize()
        create_user_command_obj.create_user(server_object, lines_of_csv)

    def removeusers(self):
        """ Method to remove users from a specific group """
        remove_users_parser_object = RemoveUserParser()
        lines_of_csv, group_name = remove_users_parser_object.remove_user_parser()
        remove_users_command_obj = RemoveUserCommand()
        signed_in_object, server_object = self.deserialize()
        remove_users_command_obj.remove_users(server_object, lines_of_csv, group_name)

    def deleteusers(self):
        """ Method to delete users from a specific group """
        delete_users_parser_object = DeleteUserParser()
        lines_of_csv = delete_users_parser_object.delete_user_parser()
        delete_users_command_obj = DeleteUserCommand()
        signed_in_object, server_object = self.deserialize()
        delete_users_command_obj.delete_users(server_object, lines_of_csv)
