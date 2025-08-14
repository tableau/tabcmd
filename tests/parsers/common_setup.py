import unittest
from unittest import mock
from tabcmd.execution import parent_parser
from collections import namedtuple
import argparse
from typing import Optional, Type, Any

__all__ = ['ParserTest', 'initialize_test_pieces', 'mock_command_action', 'encoding']

encoding = "utf-8-sig"


def mock_command_action() -> None:
    print("a mockery!")


# basically replaces tabcmd_controller:initialize_parsers
def initialize_test_pieces(commandname: str, command_object: Type[Any]) -> argparse.ArgumentParser:
    manager = parent_parser.ParentParser()
    parser_under_test = manager.get_root_parser()
    MockCommand = namedtuple("MockCommand", "name, run_command, description, define_args")
    mock_command = MockCommand(
        name=commandname,
        run_command=mock_command_action,
        description="mock help text",
        define_args=command_object.define_args
    )

    manager.include(mock_command)
    return parser_under_test


class ParserTest(unittest.TestCase):
    parser_under_test: argparse.ArgumentParser

    """
    base test cases for each parser:
    has_required_arguments
    (maybe) missing required arguments
    has optional arguments
    bad mix of optional arguments
    has unknown arguments
    """