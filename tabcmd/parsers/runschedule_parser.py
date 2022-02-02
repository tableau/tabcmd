import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser


class RunScheduleParser:
    """
    Parser to runschedule command
    """
    USER_ARG_IDX = 2
    USER_ARG_SCHEDULE_IDX = 2

    @staticmethod
    def runschedule_parser():
        """Method to parse run-schedule arguments passed by the user"""
        schedule = ""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        runschedule_parser = subparsers.add_parser('runschedule',
                                                   parents=[parser])
        try:
            schedule = sys.argv[RunScheduleParser.USER_ARG_SCHEDULE_IDX]
        except Exception as ex:
            print(ex)
        args = runschedule_parser.parse_args(sys.argv[RunScheduleParser.
                                                      USER_ARG_IDX:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args, schedule
