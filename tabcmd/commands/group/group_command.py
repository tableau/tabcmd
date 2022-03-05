from tabcmd.commands.commands import Commands


class GroupCommand(Commands):
    """
    This class acts as a base class for group related commands
    """

    @staticmethod
    def find_group_id(server, group_name):
        return Commands.get_items_by_name(server.groups, group_name)[0].id
