import argparse
import sys
import getpass
from .global_options import *
from ..logger_config import get_logger
logger = get_logger('pythontabcmd2.login_parser')



class LoginParser:
    """ Parses login arguments passed by the user"""
    @staticmethod
    def login_parser():

        parser = argparse.ArgumentParser(description='login command')
        parser.add_argument('--site', '-S', default=None, help='site of account holder' )
        parser.add_argument('--server', '-s', required=True, help='server of account holder' )
        parser.add_argument('--token', '-t', default=None, help='personal access token used to sign into the server' )
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--username', '-u', help='username of account holder')
        group.add_argument('--token-name', '-n', help='name of the personal access token used to sign into the server')
        args = parser.parse_args(sys.argv[2:])
        if args.username:
            password = getpass.getpass("Password: ")
        else:
            if args.username is None:
                password = None
        if args.token_name:
            if args.token is None:                                                      # TODO
                logger.info("please include the Personal Access Token")
                sys.exit()
        if args.site is None:
            args.site = ''
        return args, password