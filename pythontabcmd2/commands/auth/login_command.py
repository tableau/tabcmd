import sys

from .. import LoginParser
from .. import Constants
import tableauserverclient as TSC
from .. import get_logger
import json
import os
from ..commands import Commands
from .session import Session


class LoginCommand(Commands):
    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def log(self):
        logger = get_logger('pythontabcmd2.session', self.logging_level)
        return logger

    @classmethod
    def parse(cls):
        args = LoginParser.login_parser()
        return cls(args)

    def run_command(self):
        self.create_session()

    def create_session(self):
        """ Method to authenticate user and establish connection """
        logger = self.log()
        session = Session()
        if self.args.username is None and self.args.password is None or \
                self.args.token_name is None \
                and \
                self.args.token is None:
            logger.info("Please enter login credentials")
            sys.exit()
        if self.args.username or self.args.site or self.args.password or \
                self.args.server:
            session.update_session(self.args)
            session.check_for_missing_arguments()
            signed_in_object \
                = session.no_cookie_save_session_creation_with_username()

        elif self.args.token or self.args.site or self.args.token_name or \
                self.args.server:
            session.update_session(self.args)
            session.check_for_missing_arguments()
            signed_in_object \
                = session.no_cookie_save_session_creation_with_token()
        else:
            signed_in_object = session.reuse_session()
        if self.args.no_cookie:
            home_path = os.path.expanduser("~")
            file_path = os.path.join(home_path, 'tableau_auth.json')
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            session.save_token_to_json_file()
        return signed_in_object


"""
Login Scenarios to cover:
0. User forgets he has deleted credentials, and logs in without passing any 
credentials - DONE 
0: user has already logged in via username/password now wants to login via 
tokens 
0. User hasnt logged in before and just passes server:
0: User has logged in before via login command but only passes server and 
site - Prompt for password and continue
1: Login via login command using username/password -default save json
[user passes all arguments including server and site] DONE
1a. above, but user doesnt pass server or site-firsttime use of login command - prompt errrp DONE
1b. user uses login command again, doesnt pass server or site , wants to use 
whats saved DONE
2. Login via login command using PAT and Token -default save json
2a. above, but user doesnt pass server or site - take from json
2b. user uses login command again, doesnt pass server or site , wants to use 
whats saved 
3. Login via login command username/password with no cookie
3a. user has to pass server and site else error
4. Login via login command username/password with cookie 
4a. above, but user doesnt pass server or site - take from json
4b. user uses login command again, doesnt pass server or site , wants to use 
whats saved 
3. Login via login command PAT/Token with no cookie 
5. Login via login command PAT/Token with cookie 
5a. above, but user doesnt pass server or site - take from json
5b. user uses login command again, doesnt pass server or site , wants to use 
whats saved 
6. Login with individual command using username/password- default save json
6a. above, but user doesnt pass server or site - take from json
6. Login with individual command using PAT/Token -default save json
7. Login with individual command using username/password -no cookie
8. Login with individual command using PAT/Token -no cookie 
9. Login with individual command using username/password -cookie
10. Login with individual command using PAT/Token -cookie
11. Renew session if new site is passed
12. renew session if new server is passed 


"""