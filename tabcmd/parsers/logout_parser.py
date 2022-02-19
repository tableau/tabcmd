class LogoutParser:
    @staticmethod
    def logout_parser(manager, command):
        manager.include(command)
        # has no arguments
