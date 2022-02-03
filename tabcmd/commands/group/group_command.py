from ..commands import Commands
import tableauserverclient as TSC
from .. import get_logger


class GroupCommand(Commands):
    """
    This class acts as a base class for group related commands
    """
    def __init__(self, args):
        super().__init__(args)
        self.name = args.name
        self.args = args

    @staticmethod
    def find_group_id(server, group_name):
        """ Method to find the group id given group name"""
        all_groups, pagination_item = server.groups.get()
        all_group_names = [(group.name, group.id) for group in all_groups]
        group_id = None
        for group in all_group_names:
            if group[0] == group_name:
                group_id = group[1]
                break
        return group_id
