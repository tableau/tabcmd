from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class ListCommand(Server):
    """
    Command to return a list of content the user can access
    """

    name: str = "list"
    description: str = _("tabcmd.listing.short_description")

    @staticmethod
    def define_args(list_parser):
        args_group = list_parser.add_argument_group(title=ListCommand.name)
        args_group.add_argument(
            "content", choices=["projects", "workbooks", "datasources", "flows"], help=_("tabcmd.options.select_type")
        )
        args_group.add_argument("-d", "--details", action="store_true", help=_("tabcmd.options.include_details"))

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)
        content_type = args.content

        try:
            logger.info(_("tabcmd.listing.header").format(content_type, session.username))

            if content_type == "projects":
                items = server.projects.all()
            elif content_type == "workbooks":
                items = server.workbooks.all()
            elif content_type == "datasources":
                items = server.datasources.all()
            elif content_type == "flows":
                items = server.flows.all()

            if not items or len(items) == 0:
                logger.info(_("tabcmd.listing.none"))
            for item in items:
                if args.details:
                    logger.info("\t{}".format(item))
                    if content_type == "workbooks":
                        server.workbooks.populate_views(item)
                        for v in item.views:
                            logger.info(v)
                else:
                    logger.info(_("tabcmd.listing.label.id").format(item.id))
                    logger.info(_("tabcmd.listing.label.name").format(item.name))

        except Exception as e:
            Errors.exit_with_error(logger, e)
