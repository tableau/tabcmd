import sys


class Context:
    def __init__(self, parser):
        self.parser = parser

    # during normal execution, leaving input as none will default to sys.argv
    # for testing, we want to be able to pass in different updates
    def parse_inputs(self, input=None):
        parser = self.parser
        if input is None and len(sys.argv) <= 1:  # no arguments given
            parser.print_help()
            sys.exit(0)
        namespace = parser.parse_args(input)
        if not namespace.func:  # arguments did not match any command
            parser.print_help()
            sys.exit(1)

        # maybe argparse will do this?
        if namespace.func == 'help':
            parser.print_help()
            sys.exit(0)

        # if a subcommand was identified, call the function assigned to it
        # this is the functional equivalent of the call by reflection in the previous structure
        # https://stackoverflow.com/questions/49038616/argparse-subparsers-with-functions
        namespace.func(namespace).run_command(namespace)
        return namespace
