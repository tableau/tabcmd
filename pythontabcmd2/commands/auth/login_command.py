from .. import LoginParser
from .. import log
from ..commands import Commands
from .session import Session


class LoginCommand(Commands):
    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.logger = log('pythontabcmd2.login_command', self.logging_level)

    @classmethod
    def parse(cls):
        args = LoginParser.login_parser()
        return cls(args)

    def run_command(self):
        self.create_session_login_command(self.args)

    def create_session_login_command(self, args):
        """ Method to authenticate user and establish connection """
        self.logger.info("========Creating a new session========")
        session = Session()
        session.create_session(args)



"""
Login Scenarios to cover:
0: user has already logged in via username/password now wants to login via 
tokens
0: User has logged in before via login command but only passes server and 
site - Prompt for password and continue DONE
1: Login via login command using username/password -default save json
[user passes all arguments including server and site] DONE
1a. above, but user doesnt pass server or site-firsttime use of login command - 

1b. user uses login command again, doesnt pass server or site , wants to use 
whats saved DONE
2. Login via login command using PAT and Token -default save json
2a. above, but user doesnt pass server or site - take from json
2b. user uses login command again, doesnt pass server or site , wants to use 
whats saved 
3. Login via login command username/password with no cookie DONE
3a. user has pass server and site else error DONE
4. Login via login command username/password with cookie  DONE
4a. above, but user doesnt pass server or site - take from json DONE
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
