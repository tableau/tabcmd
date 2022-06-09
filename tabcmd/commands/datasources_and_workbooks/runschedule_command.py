from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class RunSchedule(DatasourcesAndWorkbooks):
    """
    This command runs the specified schedule as it is on the server.
    """

    name: str = "runschedule"
    description: str = _("runschedule.short_description")

    @staticmethod
    def define_args(runschedule_parser):
        runschedule_parser.add_argument("schedule", help=_("tabcmd.run_schedule.options.schedule"))

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        logger.info(_("export.status").format(args.schedule))
        schedule = DatasourcesAndWorkbooks.get_items_by_name(logger, server.schedules, args.schedule)[0]
        if not schedule:
            Errors.exit_with_error(logger, _("publish.errors.server_resource_not_found"))
        logger.info(_("runschedule.status"))
        Errors.exit_with_error(logger, "Not yet implemented")

        # TODO implement in REST/tsc
