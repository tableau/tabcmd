from tabcmd.commands.server import Server
import tableauserverclient as TSC


class ExtractsCommand(Server):
    """
    Base class for extracts group of commands
    """

    # TODO: this message should have the projects passed with the ds name
    # e.g instead of "regional" it should say "samples/regional"
    @staticmethod
    def print_task_scheduling_message(logger, item_type, item, action):
        logger.info("===== Scheduling extracts for {0} '{1}' to be {2} now...".format(item_type, item, action))

    @staticmethod
    def print_success_scheduled_message(logger, action, job):
        logger.info("Extract is scheduled for {0} with JobID: {1}".format(action, job.id))

    @staticmethod
    def print_success_message(logger, job: TSC.JobItem):
        logger.info("{} {} completed with status {}".format(job.type, job.id, job.finish_code))
        if job.notes:
            logger.info(job.notes)
