class GlobalOptions:
    
    @staticmethod
    def evaluate_project_path(path):
        if path[-1] != "/" :
            path = path + "/"
        newpath = path.rsplit('/')[-2]
        for directory in newpath[::-1]:
            if directory != " ":
                first_dir_from_end = newpath
                break
        return first_dir_from_end
         