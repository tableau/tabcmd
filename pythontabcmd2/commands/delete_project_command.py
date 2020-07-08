try:
    from .. import tableauserverclient as TSC
    from .. logger_config import get_logger
except:
    import tableauserverclient as TSC
    from logger_config import get_logger
logger = get_logger('pythontabcmd2.delete_project_command')

class DeleteProjectCommand:
    def __init__(self, name, parent_project_path=None):
        self.name = name
        self.parent_project_path = parent_project_path

    def delete_project(self, newserver):
        try:
            project_id = self.find_project_id(newserver, self.name)
            newserver.projects.delete(project_id)
            logger.info("Successfully deleted project") 
        except TSC.ServerResponseError as e:
            logger.info("Error: Server error occured", e) 
        except:
            logger.info("Error: Project not found, Please check project name")

    def find_project_id(self, newserver, project_name):

        all_project_items, pagination_item = newserver.projects.get()
        all_project_names = [(proj.name, proj.id) for proj in all_project_items]
        project_id = None
        for project in all_project_names:
            if project[0] == project_name:
                project_id = project[1]
                break
        return project_id
    