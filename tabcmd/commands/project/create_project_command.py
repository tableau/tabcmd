import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class CreateProjectCommand(Server):
    """
    Command to create a project
    """

    name: str = "createproject"
    description: str = _("createproject.short_description")

    @staticmethod
    def define_args(create_project_parser):
        args_group = create_project_parser.add_argument_group(title=CreateProjectCommand.name)
        args_group.add_argument(
            "--name", "-n", dest="project_name", required=True, help=_("createproject.options.name")
        )
        set_parent_project_arg(create_project_parser)
        set_description_arg(create_project_parser)

    @classmethod
    def run_command(cls, args):
        logger = log(cls.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)
        parent_id = None
        readable_name = args.project_name
        if args.parent_project_path:
            try:
                logger.info(_("tabcmd.find.parent_project").format(args.parent_project_path))
                parent = Server.get_project_by_name_and_parent_path(logger, server, None, args.parent_project_path)
            except Exception as e:
                Errors.exit_with_error(logger, exception=e)
            readable_name = "{0}/{1}".format(args.parent_project_path, args.project_name)
            parent_id = parent.id
            logger.debug("parent project = `{0}`, id = {1}".format(args.parent_project_path, parent_id))
        logger.info(_("createproject.status").format(readable_name))
        new_project = TSC.ProjectItem(args.project_name, args.description, None, parent_id)
        project_item = None
        try:
            project_item = server.projects.create(new_project)
            logger.info(_("common.output.succeeded"))
            return project_item
        except Exception as e:
            if Errors.is_resource_conflict(e) and args.continue_if_exists:
                logger.info(_("tabcmd.result.already_exists").format(_("content_type.project"), args.project_name))
                logger.info(_("common.output.succeeded"))
            else:
                Errors.exit_with_error(logger, exception=e)

        return project_item
