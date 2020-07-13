try:
    from .. import tableauserverclient as TSC
    from ..logger_config import get_logger
except:
    import tableauserverclient as TSC
    from logger_config import get_logger
logger = get_logger('pythontabcmd2.create_group_command')


class CreateGroupCommand:
    def __init__(self, name):
        self.name = name

    def create_group(self, newserver):
        try:
            new_group = TSC.GroupItem(self.name)
            newserver.groups.create(new_group)
            logger.info("Successfully created group")
        except TSC.ServerResponseError as e:
            logger.info("Error: Server error occurred: Group already exists")
