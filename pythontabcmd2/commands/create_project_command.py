
try:
    from .. import tableauserverclient as TSC
    from .. logger_config import get_logger
except:
    import tableauserverclient as TSC
    from logger_config import get_logger
logger = get_logger('pythontabcmd2.create_project_command')


class CreateProjectCommand:
    def __init__(self, name, description=None, content_permission=None, parent_path_name=None):
        self.name = name
        self.description= description
        self.content_permission = content_permission
        self.parent_path_name = parent_path_name

    def create_project(self, newserver):
        """Method to create project using tableauserverclient methods"""
        project_path = self.find_project_id(newserver, self.parent_path_name)
        top_level_project = TSC.ProjectItem(self.name, self.description, self.content_permission, project_path)
        top_level_project = self.create_project_helper(newserver, top_level_project)
        
    def create_project_helper(self, server, project_item):
        """ Helper method to catch server errors thrown by tableauserverclient"""
        try:
            project_item = server.projects.create(project_item)
            logger.info('Successfully created a new project called: %s' % project_item.name)
            return project_item
        except TSC.ServerResponseError as e:
            logger.info('Error: We have already created this project: %s' % project_item.name)

    def find_project_id(self, newserver, parent_path_name):                 # TODO: MOVE TO SEPARATE CLASS 
        """ Method to find project id given parent path name """
        all_project_items, pagination_item = newserver.projects.get()
        all_project_names = [(proj.name, proj.id) for proj in all_project_items]
        project_id = None
        for project in all_project_names:
            if project[0] == parent_path_name:
                project_id = project[1]
                break
        return project_id

