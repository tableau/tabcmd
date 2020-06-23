import argparse
import sys
import shlex
import getpass

class LoginParser:
    
    def login_parser(self):
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
        elif args.username is None:
            password = None
        if args.token_name:
            if args.token is None:
                print("please include the Personal Access Token")
                sys.exit()
        if args.site is None:
            args.site = ''
        return args.username, password, args.site, args.server, args.token_name, args.token


    