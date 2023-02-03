import polling2  # type: ignore
import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.extracts.extracts import Extracts
from tabcmd.commands.server import Server
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class RefreshExtracts(Server):

    name: str = "refreshextracts"
    description: str = _("refreshextracts.short_description")

    @staticmethod
    def define_args(refresh_extract_parser):
        group = refresh_extract_parser.add_argument_group(title=RefreshExtracts.name)
        set_ds_xor_wb_args(group, True)
        set_incremental_options(group)
        set_calculations_options(group)
        set_project_arg(group)
        set_parent_project_arg(group)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)

        if args.addcalculations or args.removecalculations:
            logger.warning(
                "Add Calculations tasks are deprecated and this parameter has no effect."
                "It will be replaced with Workbook Acceleration in a future update."
            )

        # are these two mandatory? mutually exclusive?
        # docs: the REST method always runs a full refresh even if the refresh type is set to incremental.
        if args.incremental:  # docs: run the incremental refresh
            logger.warn("Incremental refresh is not yet available through the new tabcmd")
        # if args.synchronous:  # docs: run a full refresh and poll until it completes
        # else:  run a full refresh but don't poll for completion

        try:
            item = Extracts.get_wb_or_ds_for_extracts(args, logger, server)
            if args.datasource:
                logger.info(_("refreshextracts.status_refreshed").format(_("content_type.datasource"), args.datasource))
                job: TSC.JobItem = server.datasources.refresh(item.id)
            else:
                job: TSC.JobItem = server.workbooks.refresh(item.id)
                logger.info(_("refreshextracts.status_refreshed").format(_("content_type.workbook"), args.workbook))

        except Exception as e:
            Errors.exit_with_error(logger, _("refreshextracts.errors.error"), e)

        logger.info(_("common.output.job_queued_success"))
        logger.debug("Extract refresh queued with JobID: {}".format(job.id))

        if args.synchronous:
            # maintains a live connection to the server while the refresh operation is underway, polling every second
            # until the background job is done.   <job id="JOB_ID" mode="MODE" type="RefreshExtract" />
            logger.info("Waiting for refresh job to begin ....")

            try:
                polling2.poll(lambda: logger.info(".") and job.started_at is not None, step=1, timeout=args.timeout)
            except polling2.TimeoutException as te:
                Errors.exit_with_error(logger, _("messages.timeout_error.summary"))
            logger.info("Job started at {}".format(job.started_at))

            try:
                polling2.poll(
                    lambda: logger.info("{}".format(job.progress)) and job.finish_code != -1,
                    step=1,
                    timeout=args.timeout,
                )
                logger.info("Job completed at {}".format(job.completed_at))
            except polling2.TimeoutException as te:
                Errors.exit_with_error(logger, _("messages.timeout_error.summary"))

        else:
            logger.info(_("common.output.job_queued_success"))
            logger.debug("Extract refresh started with JobID: {0}".format(job.id))
