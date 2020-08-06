import argparse
from .parent_parser import ParentParser


class CommonParser:
    def common_parser_arguments(self):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--parent-project-path',
                            default=None,
                            help='path of parent project')
        return parser
