import argparse


class ParentParser:
    def parent_parser_with_global_options(self):

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--server', '-s',
                            help='server of account holder')
        parser.add_argument('--user', '-u',
                            help='username of account holder')
        parser.add_argument('--site', '-t', default=None,
                            help='site of account holder')
        parser.add_argument('--password', '-p',
                            help='password of account holder')
        parser.add_argument('--no-prompt', default=None,
                            help='no prompt for password')
        parser.add_argument('--logging-level', '-l',
                            choices=['debug', 'info', 'error'],
                            default='info',
                            help='desired logging level '
                                 '(set to error by default)')
        return parser

