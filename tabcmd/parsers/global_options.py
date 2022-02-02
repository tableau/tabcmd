class GlobalOptions:
    """ Class to evaluate global options for example: project path"""
    LAST_INDEX = 1
    SECOND_INDEX_FROM_END = 2

    @staticmethod
    def evaluate_project_path(path):
        """ Method to parse the project path provided by the user"""
        first_dir_from_end = None
        if path[-GlobalOptions.LAST_INDEX] != "/":
            path = path + "/"
        new_path = path.rsplit('/')[-GlobalOptions.SECOND_INDEX_FROM_END]
        for directory in new_path[::-GlobalOptions.LAST_INDEX]:
            if directory != " ":
                first_dir_from_end = new_path
                break
        return first_dir_from_end
