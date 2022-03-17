from tabcmd.commands.commands import Commands


class GroupCommand(Commands):
    """
    This class acts as a base class for group related commands
    """

    @staticmethod
    def find_group_id(logger, server, group_name):
        return Commands.get_items_by_name(logger, server.groups, group_name)[0].id
