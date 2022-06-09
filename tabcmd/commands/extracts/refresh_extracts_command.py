import polling2  # type: ignore
import tableauserverclient as TSC

from tabcmd.execution.global_options import *
from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log
from tabcmd.execution.localize import _


class RefreshExtracts(Server):

    name: str = "refreshextracts"
    description: str = "Refresh the extracts of a workbook or datasource on the server"

    @staticmethod
    def define_args(refresh_extract_parser):
        possible_targets = set_ds_xor_wb_args(refresh_extract_parser)
        possible_targets.add_argument(
            "--url",
            help="The name of the workbook as it appears in the URL. A workbook published as “Sales Analysis” \
            has a URL name of “SalesAnalysis”.",
        )

        set_incremental_options(refresh_extract_parser)
        set_calculations_options(refresh_extract_parser)
        set_project_arg(refresh_extract_parser)
        set_parent_project_arg(refresh_extract_parser)

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args)
        refresh_action = "refresh"

        if args.addcalculations or args.removecalculations:
            logger.warning(
                "Data Acceleration tasks are deprecated and this parameter has no effect."
                "It will be removed in a future update."
            )

        # are these two mandatory? mutually exclusive?
        # docs: the REST method always runs a full refresh even if the refresh type is set to incremental.
        if args.incremental:  # docs: run the incremental refresh
            logger.warn("Incremental refresh is not yet available through the new tabcmd")
        # if args.synchronous:  # docs: run a full refresh and poll until it completes
        # else:  run a full refresh but don't poll for completion

        container = None
        if args.project_name:
            try:
                container = Server.get_project_by_name_and_parent_path(
                    logger, server, args.project_name, args.parent_project_path
                )
            except Exception as ex:
                logger.warning(
                    "Could not find project {}/{}. Continuing without.".format(
                        args.parent_project_path, args.project_name
                    )
                )
        job = None
        try:
            # TODO: use the container in the search
            if args.datasource:
                logger.debug("Finding datasource `{}` on the server...".format(args.datasource))
                datasource_id = Server.get_data_source_id(logger, server, args.datasource, container)
                logger.info(_("refreshextracts.status_refreshed").format(_("content_type.datasource"), args.datasource))
                job: TSC.JobItem = server.datasources.refresh(datasource_id)

            elif args.workbook:
                logger.debug("Finding workbook `{}` on the server...".format(args.workbook))
                workbook_id = Server.get_workbook_id(logger, server, args.workbook, container)
                logger.info(_("refreshextracts.status_refreshed").format(_("content_type.workbook"), args.workbook))
                job: TSC.JobItem = server.workbooks.refresh(workbook_id)

            elif args.url:
                logger.error("URL not yet implemented")

        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, "Error scheduling extract refresh", e)

        logger.info(_("common.output.job_queued_success"))

        if args.synchronous:
            # maintains a live connection to the server while the refresh operation is underway, polling every second
            # until the background job is done.   <job id="JOB_ID" mode="MODE" type="RefreshExtract" />
            logger.info("Waiting for refresh job to begin ....")

            try:
                polling2.poll(lambda: logger.info(".") and job.started_at is not None, step=1, timeout=args.timeout)
            except polling2.TimeoutException as te:
                Errors.exit_with_error(
                    logger,
                    "Timed out waiting for the refresh task to begin running. To wait longer until the job starts, try removing the --timeout.",
                )
            logger.info("Job started at {}".format(job.started_at))

            try:
                polling2.poll(
                    lambda: logger.info("{}".format(job.progress)) and job.finish_code != -1,
                    step=1,
                    timeout=args.timeout,
                )
                logger.info("Job completed at {}".format(job.completed_at))
            except polling2.TimeoutException as te:
                Errors.exit_with_error(logger, "Timed out waiting for the refresh task to complete.")

        else:
            logger.info(_("common.output.job_queued_success"))
            logger.debug("Extract refresh started with JobID: {0}".format(job.id))
