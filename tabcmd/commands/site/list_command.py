import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class ListCommand(Server):
    """
    Command to return a list of content the user can access
    """

    name: str = "list"
    description: str = "List content items of a specified type"

    @staticmethod
    def define_args(list_parser):
        args_group = list_parser.add_argument_group(title=ListCommand.name)
        args_group.add_argument("content", choices=["projects", "workbooks", "datasources"], help="View content")

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)
        content_type = args.content

        try:
            logger.info("===== Listing {0} content for user {1}...".format(content_type, session.username))
            try:
                if content_type == "projects":
                    items = server.projects.all()
                elif content_type == "workbooks":
                    items = server.workbooks.all()
                elif content_type == "datasources":
                    items = server.datasources.all()
            except TSC.ServerResponseError as e:
                Errors.exit_with_error(logger, exception=e)

            logger.info("===== Listing {0} content for user {1}...".format(content_type, session.username))
            for item in items:
                logger.info("NAME:".rjust(10), item.name)
                logger.info("ID:".rjust(10), item.id)

        except Exception as e:
            Errors.exit_with_error(logger, e)
