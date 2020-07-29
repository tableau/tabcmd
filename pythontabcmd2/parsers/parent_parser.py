import argparse
class ParentParser:
    def parent_parser_with_global_options(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--server', '-s', help='foo help')
        return parser