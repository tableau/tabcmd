import argparse
import sys
import shlex
import getpass


class CreateProjectParser:
    
    def create_project_parser(self):
        parser = argparse.ArgumentParser(description='create project command')
            
        parser.add_argument('--name','-n', required=True, help='name of project')
        parser.add_argument('--parent-project-path','-p', default=None, help='id of parent project')
        parser.add_argument('--description','-d', default=None, help='description of project')
        parser.add_argument('--content-permission','-c', default=None, help='content permission of project')

        args = parser.parse_args(sys.argv[2:])

        return args.name, args.description, args.content_permission, args.parent_project_path