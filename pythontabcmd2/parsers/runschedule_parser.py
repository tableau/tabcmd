import argparse
import sys
from .global_options import *
from .parent_parser import ParentParser


class RunScheduleParser:
    @staticmethod
    def runschedule_parser():
        """Method to parse run-schedule arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        subparsers = parser.add_subparsers()
        runschedule_parser = subparsers.add_parser('runschedule',
                                                         parents=[parser])
        schedule = sys.argv[2]
        args = runschedule_parser.parse_args(sys.argv[2:])
        if args.site is None or args.site == "Default":
            args.site = ''
        return args, schedule
