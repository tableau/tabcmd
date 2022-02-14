import sys
from tabcmd.execution.parent_parser import ParentParser


class RunScheduleParser:
    """
    Parser to runschedule command
    """
    USER_ARG_IDX = 2
    USER_ARG_SCHEDULE_IDX = 2

    @staticmethod
    def runschedule_parser():
        """Method to parse run-schedule arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        runschedule_parser = subparsers.add_parser('runschedule', parents=[parser])

        args = runschedule_parser.parse_args(sys.argv[RunScheduleParser.USER_ARG_IDX:])
        try:
            args.schedule = sys.argv[RunScheduleParser.USER_ARG_SCHEDULE_IDX]
        except Exception as ex:
            print(ex)
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
