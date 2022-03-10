from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log
from .datasources_and_workbooks_command import DatasourcesAndWorkbooks


class RunSchedule(DatasourcesAndWorkbooks):
    """
    This command runs the specified schedule as it is on the server.
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        server = session.create_session(args)
        logger.info("Finding schedule {} on server...".format(args.schedule))
        schedule = DatasourcesAndWorkbooks.get_items_by_name(server.schedules, args.schedule)[0]
        if not schedule:
            DatasourcesAndWorkbooks.exit_with_error(logger, "Could not find schedule")
        logger.info("Found schedule")
        DatasourcesAndWorkbooks.exit_with_error(logger, "Not yet implemented")

        # TODO implement in REST/tsc
