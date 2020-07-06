
try:
    from .. import tableauserverclient as TSC
    from .. logger_config import get_logger
except:
    import tableauserverclient as TSC
    from logger_config import get_logger
logger = get_logger('pythontabcmd2.create_project')

class CreateProject:
    def __init__(self, name, description=None, content_permission=None, parent_id=None):
        self.name = name
        self.description= description
        self.content_permission = content_permission
        self.parent_id = parent_id

    def create_project(self, newserver):
        top_level_project = TSC.ProjectItem(self.name, self.description, self.content_permission,self.parent_id)
        top_level_project = self.create_project_helper(newserver, top_level_project)
        
    def create_project_helper(self, server, project_item):
        try:
            project_item = server.projects.create(project_item)
            logger.info('Successfully created a new project called: %s' % project_item.name)
            return project_item
        except TSC.ServerResponseError:
            logger.info('Error: We have already created this project: %s' % project_item.name)