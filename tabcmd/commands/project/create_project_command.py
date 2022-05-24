import tableauserverclient as TSC

from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log
from tabcmd.commands.constants import Errors
from tabcmd.execution.localize import _


class CreateProjectCommand(Server):
    """
    Command to create a project
    """

    name: str = "createproject"
    description: str = _("createproject.short_description")

    @staticmethod
    def define_args(create_project_parser):
        create_project_parser.add_argument(
            "--name", "-n", dest="project_name", required=True, help=_("createproject.options.name")
        )
        set_parent_project_arg(create_project_parser)
        set_description_arg(create_project_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        parent_id = None
        readable_name = args.project_name
        if args.parent_project_path:
            try:
                logger.info(_("tabcmd.find.parent_project").format(args.parent_project_path))
                parent = Server.get_project_by_name_and_parent_path(logger, server, None, args.parent_project_path)
            except TSC.ServerResponseError as exc:
                Errors.exit_with_error(logger, _("publish.errors.server_resource_not_found"), exc)
            readable_name = "{0}/{1}".format(args.parent_project_path, args.project_name)
            parent_id = parent.id
            logger.debug("parent project = `{0}`, id = {1}".format(args.parent_project_path, parent_id))
        logger.info(_("createproject.status").format(readable_name))
        new_project = TSC.ProjectItem(args.project_name, args.description, None, parent_id)
        try:
            project_item = server.projects.create(new_project)
            logger.info(_("common.output.succeeded"))
            return project_item
        except TSC.ServerResponseError as e:
            if Errors.is_resource_conflict(e):
                if args.continue_if_exists:
                    logger.info(_("tabcmd.result.already_exists").format(args.project_name))
                    return
                else:
                    Errors.exit_with_error(logger, _("tabcmd.result.already_exists").format(args.project_name))
            Errors.exit_with_error(logger, _("publish.errors.unexpected_server_response"), e)
