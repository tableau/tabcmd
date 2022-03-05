from tabcmd.commands.commands import Commands
import tableauserverclient as TSC

class ProjectCommand(Commands):
    @staticmethod
    def get_project_by_name_and_parent_path(server, project_name, parent_path):
        # print("get by name and path: {0}, {1}".format(project_name, parent_path))
        project = None
        if not project_name:
            project = ProjectCommand._get_parent_project_from_tree(
                server, ProjectCommand._parse_project_path_to_list(parent_path)
            )
        else:
            hierarchy = ProjectCommand._parse_project_path_to_list(parent_path)
            project = ProjectCommand._get_project_by_name_and_parent(
                server, project_name, ProjectCommand._get_parent_project_from_tree(server, hierarchy)
            )
        if not project:
            raise TSC.server.ServerResponseError(
                "404", "Could not find project", "{0}/{1}".format(parent_path, project_name)
            )
        return project

    @staticmethod
    def _parse_project_path_to_list(project_path):
        if project_path is None:
            return []
        return project_path.split("/")

    @staticmethod
    def _get_project_by_name_and_parent(server, project_name, parent):
        # print("get by name and parent: {0}, {1}".format(project_name, parent))
        # get by name to narrow down the list
        projects = ProjectCommand.get_items_by_name(server.projects, project_name)
        if parent is not None:
            parent_id = parent.id
            for project in projects:
                if project.parent_id == parent_id:
                    return project
        return projects[0]

    @staticmethod
    def _get_parent_project_from_tree(server, hierarchy):
        # print("get from tree: {0}".format(hierarchy))
        tree_height = len(hierarchy)
        if tree_height == 0:
            return None
        elif tree_height == 1:
            return ProjectCommand._get_project_by_name_and_parent(server, hierarchy[0], None)
        else:
            name = hierarchy.pop(tree_height - 1)
            return ProjectCommand._get_project_by_name_and_parent(
                server, name, ProjectCommand._get_parent_project_from_tree(server, hierarchy)
            )
