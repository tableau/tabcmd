from tabcmd.commands.server import Server


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
    def print_success_message(logger, action, job):
        logger.info("Extract {0} started with JobID: {1}".format(action, job.id))
