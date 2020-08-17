import argparse
from .parent_parser import ParentParser


class CommonParser:
    def common_parser_arguments(self):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--parent-project-path',
                            default=None,
                            help='path of parent project')
        return parser

    @staticmethod
    def read_file(file_name):
        csv_lines = None
        try:
            with open(file_name) as f:
                csv_lines = [line.strip() for line in f.readlines()]
            f.close()
        except IOError:
            print("File not found")
        return csv_lines
