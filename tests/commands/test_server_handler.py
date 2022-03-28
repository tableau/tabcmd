import unittest
import logging

from tabcmd.commands.server import Server


# TODO add checks that the logger was called?
class ServerTests(unittest.TestCase):

    def test_exit_with_logger_problem(self):
        try:
            Server.exit_with_error(None, "a message appears")
        except SystemExit as um:
            assert(um.code == 1)

    def test_exit_with_message(self):
        try:
            log = logging.getLogger("exitwithmessage")
            Server.exit_with_error(log, "a message appears")
        except SystemExit as um:
            assert(um.code == 1)

    def test_exit_with_exception(self):
        try:
            log = logging.getLogger("exitwithexception")
            Server.exit_with_error(log, "a message appears")
        except SystemExit as um:
            assert(um.code == 1)

