from src.execution import parent_parser
from collections import namedtuple


def mock_command_action():
    print("a mockery!")


# basically replaces tabcmd_controller:initialize_parsers
def initialize_test_pieces(commandname, command_object):
    manager = parent_parser.ParentParser()
    parser = manager.get_root_parser()
    mock_command = namedtuple("TestObject", "name, run_command, description, define_args")
    mock_command.name = commandname
    mock_command.run_command = mock_command_action
    mock_command.description = "mock help text"
    mock_command.define_args = command_object.define_args

    manager.include(mock_command)
    return parser


"""
 base test cases for each parser:
 has_required_arguments
 (maybe) missing required arguments
 has optional arguments
 bad mix of optional arguments
 has unknown arguments
 """
