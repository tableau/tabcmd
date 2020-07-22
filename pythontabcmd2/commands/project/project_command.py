from commands.commands import Commands


class ProjectCommand(Commands):

    def __init__(self, args, evaluated_project_path):
        self.name = args.name
        self.parent_path_name = evaluated_project_path

    @staticmethod
    def find_project_id(server, parent_path_name):
        """ Method to find project id given parent path name """
        all_project_items, pagination_item = server.projects.get()
        all_project_names = [(proj.name, proj.id) for proj in all_project_items]
        project_id = None
        for project in all_project_names:
            if project[0] == parent_path_name:
                project_id = project[1]
                break
        return project_id
