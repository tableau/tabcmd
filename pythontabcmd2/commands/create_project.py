
try:
    from .. import tableauserverclient as TSC
except:
    import tableauserverclient as TSC  

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
            print('Created a new project called: %s' % project_item.name)
            print("*****Successfully created project*****")
            return project_item
        except TSC.ServerResponseError:
            print('Error: We have already created this project: %s' % project_item.name)