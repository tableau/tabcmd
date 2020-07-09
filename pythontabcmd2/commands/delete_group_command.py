try:
    from .. import tableauserverclient as TSC
    from .. logger_config import get_logger
except:
    import tableauserverclient as TSC
    from logger_config import get_logger
logger = get_logger('pythontabcmd2.delete_group_command')

class DeleteGroupCommand:
    def __init__(self, name):
        self.name = name

    def delete_group(self, newserver):
        try:
            group_id = self.find_group_id(newserver, self.name)
            newserver.groups.delete(group_id)
            logger.info("Successfully deleted group") 
        except TSC.ServerResponseError as e:
            logger.info("Error: Server error occured", e) 
        except:
            logger.info("Error: Group not found, Please check Group name")

    def find_group_id(self, newserver, group_name):
        all_groups, pagination_item = newserver.groups.get()
        all_group_names = [(group.name, group.id) for group in all_groups]
        group_id = None
        for group in all_group_names:
            if group[0] == group_name:
                group_id = group[1]
                break
        return group_id
    