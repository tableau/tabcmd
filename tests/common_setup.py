from tabcmd.execution import parent_parser


def mock_command_action():
    print('a mockery!')


# basically replaces tabcmd_controller:initialize_parsers
def initialize_test_pieces(commandname):
    manager = parent_parser.ParentParser()
    parser = manager.get_root_parser()
    mock_command = commandname, mock_command_action, 'mock help text'
    return parser, manager, mock_command


"""
 base test cases for each parser:
 has_required_arguments
 (maybe) missing required arguments
 has optional arguments
 bad mix of optional arguments
 has unknown arguments
 """
