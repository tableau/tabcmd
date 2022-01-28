class GlobalOptions:
    """ Class to evaluate global options for example: project path"""
    @staticmethod
    def evaluate_project_path(path):
        """ Method to parse the project path provided by the user"""
        first_dir_from_end = None
        if path[-1] != "/":
            path = path + "/"
        new_path = path.rsplit('/')[-2]
        for directory in new_path[::-1]:
            if directory != " ":
                first_dir_from_end = new_path
                break
        return first_dir_from_end
