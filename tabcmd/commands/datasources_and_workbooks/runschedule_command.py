from tabcmd.execution.logger_config import log
from ..auth.session import Session
from tabcmd.parsers.runschedule_parser import RunScheduleParser
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class RunSchedule(DatasourcesAndWorkbooks):
    """
    This command runs the specified schedule as it is on the server.
    """

    @classmethod
    def parse(cls):
        args = RunScheduleParser.runschedule_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server_object = session.create_session(args)
        # TODO implement
