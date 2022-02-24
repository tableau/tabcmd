class CreateGroupParser:
    """
    Parser for creategroup command
    """

    @staticmethod
    def create_group_parser(manager, command):
        """Method to parse create group arguments passed by the user"""
        create_group_parser = manager.include(command)
        create_group_parser.add_argument('name')
