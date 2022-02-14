import sys
from tabcmd.execution.global_options import *
from tabcmd.execution.parent_parser import ParentParser
from tabcmd.execution.common_parser import CommonParser


class PublishParser(ParentParser):
    """Parser to the command publish"""
    USER_ARG_IDX = 3
    USER_ARG_SOURCE_IDX = 2
    USER_ARG_FILE_NAME_IDX = 2

    @staticmethod
    def publish_parser():
        """Method to parse publish arguments passed by the user"""
        parent_parser = ParentParser()
        parser = parent_parser.parent_parser_with_global_options()
        common_parser_obj = CommonParser()

        common_parser = common_parser_obj.common_parser_arguments()
        subparsers = parser.add_subparsers()
        publish_parser = subparsers.add_parser('publish',
                                               parents=[parser,
                                                        common_parser])
        publish_parser.add_argument('--name', '-n',
                                    help='Name of the workbook or '
                                         'data source on the server')
        publish_parser.add_argument('--overwrite', '-o', action='store_true',
                                    help='Overwrites the workbook, '
                                         'data source, or data extract '
                                         'if it already exists on '
                                         'the server.')
        # make overwrite and append flags mutually exclusive
        publish_parser.add_argument('--project', '-r', default=None,
                                    help='Publishes the workbook, '
                                         'data source, or data extract'
                                         ' into the specified project')
        publish_parser.add_argument('--db-username',
                                    help='Use this option to publish a '
                                         'database user name with the '
                                         'workbook,'
                                         ' data source, or data extract.')
        publish_parser.add_argument('--db-password',
                                    help=' publish a database password '
                                         'with the workbook, data source, '
                                         'or extract')
        publish_parser.add_argument('--tabbed', action='store_true',
                                    help='When a workbook with tabbed '
                                         'views is published, each sheet'
                                         ' becomes a tab that viewers can '
                                         'use to navigate through '
                                         'the workbook')

        args = publish_parser.parse_args(sys.argv[PublishParser.USER_ARG_IDX:])
        args.source = str(sys.argv[PublishParser.USER_ARG_SOURCE_IDX])
        args.filename = (sys.argv[PublishParser.USER_ARG_FILE_NAME_IDX])
        if args.parent_project_path is not None:
            args.evaluated_project_path = GlobalOptions.evaluate_project_path(args.parent_project_path)
        else:
            args.evaluated_project_path = args.parent_project_path
        if args.site is None or args.site == "Default":
            args.site = ''
        return args
