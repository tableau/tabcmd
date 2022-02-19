import sys


class RunScheduleParser:
    """
    Parser to runschedule command
    """

    @staticmethod
    def runschedule_parser(manager, command):
        """Method to parse run-schedule arguments passed by the user"""
        runschedule_parser = manager.include(command)
        runschedule_parser.add_argument('schedule', help='name of schedule')
