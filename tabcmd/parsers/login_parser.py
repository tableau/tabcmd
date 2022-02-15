class LoginParser:
    """ Parses login arguments passed by the user"""

    @staticmethod
    def login_parser(manager, command):
        login_parser = manager.include(command)
        # just uses global options
