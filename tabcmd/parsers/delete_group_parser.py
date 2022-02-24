class DeleteGroupParser:
    """
    Parser for the command deletegroup
    """

    @staticmethod
    def delete_group_parser(manager, command):
        """Method to parse delete group arguments passed by the user"""
        delete_group_parser = manager.include(command)
        delete_group_parser.add_argument("name", help="name of group to delete")
