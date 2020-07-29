class GlobalOptions:

    @staticmethod
    def evaluate_project_path(path):
        """ Method to parse the project path provided by the user"""
        if path[-1] != "/":
            path = path + "/"
        new_path = path.rsplit('/')[-2]
        for directory in new_path[::-1]:
            if directory != " ":
                first_dir_from_end = new_path
                break
        return first_dir_from_end
