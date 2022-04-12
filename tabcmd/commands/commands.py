import os
import sys
import tableauserverclient as TSC


class Commands:
    def __init__(self, args):
        self.logger = None
        self.username = args.username
        self.password = args.password
        self.server = args.server
        self.site = args.site
        self.token_name = args.token_name
        self.personal_token = args.token
        self.logging_level = args.logging_level
