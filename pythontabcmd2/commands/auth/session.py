from parsers.login_parser import LoginParser

try:
    from tabcmd2.pythontabcmd2 import tableauserverclient as TSC
    from constants import Constants
    from logger_config import get_logger
except:
    import tableauserverclient as TSC
    from constants import Constants
    from logger_config import get_logger
import os
import dill as pickle
logger = get_logger('pythontabcmd2.session')


class Session:
    def __init__(self, args, password):
        self.username = args.username
        self.password = password 
        self.server = args.server
        self.site = args.site
        self.token_name = args.token_name
        self.personal_token = args.token

    @classmethod
    def parse(cls):
        args, password = LoginParser.login_parser()
        return cls(args, password)

    def run_command(self):
        self.create_session()


    def create_session(self):
        """ Method to authenticate user and establish connection """
        if self.username: 
            try: 
                tableau_auth = TSC.TableauAuth(self.username, self.password, self.site)
                tableau_server = TSC.Server(self.server, use_server_version=True)
                signed_in_object = tableau_server.auth.sign_in(tableau_auth)
                self.pickle_auth_objects(signed_in_object, tableau_server)
                logger.info("=======Successfully established connection=======")
            except TSC.ServerResponseError as e:
                if e.code == Constants.login_error:
                    logger.info("Login Error, Please Login again")

        elif self.token_name:
            try:
                tableau_auth = TSC.PersonalAccessTokenAuth(self.token_name, self.personal_token, self.site)
                tableau_server = TSC.Server(self.server, use_server_version=True)
                signed_in_object = tableau_server.auth.sign_in_with_personal_access_token(tableau_auth)
                self.pickle_auth_objects(signed_in_object, tableau_server)
                logger.info("=======Successfully established connection=======")
            except TSC.ServerResponseError as e:
                if e.code == Constants.login_error:
                    logger.info("Login Error, Please Login again")

    def pickle_auth_objects(self, signed_in_object, tableau_server):
        """ Method to pickle signed in object and tableau server object """
        signed_in_object_str= str(signed_in_object)
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, 'tabcmd.pkl')
        with open(str(file_path), 'wb') as output:
            pickle.dump(signed_in_object_str, output, pickle.HIGHEST_PROTOCOL)
            pickle.dump(tableau_server, output, pickle.HIGHEST_PROTOCOL)
        

