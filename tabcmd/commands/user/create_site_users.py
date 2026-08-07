import tableauserverclient as TSC
from tableauserverclient.server.endpoint.exceptions import JobFailedException

from tabcmd.commands.auth.session import Session
from tabcmd.commands.constants import Errors
from tabcmd.execution.global_options import *
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .user_data import UserCommand


class CreateSiteUsersCommand(UserCommand):
    """
    Command to add users to a site, based on information supplied in a comma-separated values (CSV) file.
    If the user is not already created on the server, the command creates the user before adding
    that user to the site
    """

    name: str = "createsiteusers"
    description: str = _("createsiteusers.short_description")

    @staticmethod
    def define_args(create_site_users_parser):
        args_group = create_site_users_parser.add_argument_group(title=CreateSiteUsersCommand.name)
        UserCommand.set_role_arg(args_group)
        set_users_file_positional(args_group)
        set_completeness_options(args_group)
        UserCommand.set_auth_arg(args_group)
        set_no_wait_option(args_group)
        set_silent_option(args_group)

    @classmethod
    def run_command(cls, args):
        logger = log(cls.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        server = session.create_session(args, logger)

        creation_site = "current site"

        # Pre-flight validation. Under --complete (default) any CSV-shape error
        # aborts the whole run before submission -- matching Classic's
        # with_transaction semantics as closely as we can without server support.
        # Under --no-complete we validate leniently and let the server sort out
        # remaining issues per-row.
        UserCommand.validate_file_for_import(args.filename, logger, detailed=True, strict=args.require_all_valid)

        if not args.silent_progress:
            logger.info(_("addusers.status").format(args.filename.name, creation_site))

        user_obj_list = UserCommand.get_users_from_file(args.filename, logger)
        if not user_obj_list:
            logger.info(_("importcsvsummary.line.processed").format(0))
            return

        # Apply command-line overrides to every user object before submitting.
        for user_obj in user_obj_list:
            if args.role:
                user_obj.site_role = args.role  # tsc is case sensitive
            if args.auth_type:
                user_obj.auth_setting = args.auth_type

        # Submit as a single bulk import job. Server returns a JobItem tracking
        # the async processing on its side.
        try:
            job = server.users.bulk_add(user_obj_list)
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(logger, exception=e)
            return

        if not args.silent_progress:
            logger.info(_("importcsvsummary.job.queued").format(job.id))

        if args.nowait:
            # Fire and forget. Server processes the job asynchronously; caller
            # can query with `tabcmd get job/<id>` or via the REST API.
            return

        # Wait for the server-side job to finish. Under --silent-progress the
        # framework's own debug logging is still emitted but we skip our own
        # per-completion summary.
        try:
            job_done = server.jobs.wait_for_job(job_id=job.id, timeout=args.timeout)
        except JobFailedException as je:
            Errors.exit_with_error(logger, exception=je)
            return
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)
            return

        if args.silent_progress:
            return

        # Summarize per-row outcomes. `status_notes` is populated for
        # UserImport jobs; each entry is a dict with keys type/value/text.
        # The specific types the server emits are documented at
        # https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_jobs_tasks_and_schedules.htm#query_job
        # (CountOfUsersAddedToSite, CountOfUsersSkipped, etc.). If a caller
        # is on an older TSC that doesn't expose status_notes, fall back to
        # the generic notes list.
        status_notes = getattr(job_done, "status_notes", None) or []
        summary_counts = {}
        for note in status_notes:
            note_type = note.get("type")
            note_value = note.get("value")
            if note_type and note_value is not None:
                summary_counts[note_type] = note_value

        added = int(summary_counts.get("CountOfUsersAddedToSite", 0) or 0)
        skipped = int(summary_counts.get("CountOfUsersSkipped", 0) or 0)
        processed = int(summary_counts.get("CountOfUsersProcessed", len(user_obj_list)) or 0)

        logger.info(_("importcsvsummary.line.processed").format(processed))
        logger.info(_("importcsvsummary.line.skipped").format(skipped))
        logger.info(_("importcsvsummary.users.added.count").format(added))

        # Detailed per-row errors: any statusNote whose type isn't a
        # CountOf* aggregate is likely a per-row message the user should see.
        detail_notes = [n for n in status_notes if not (n.get("type") or "").startswith("CountOf")]
        if detail_notes or job_done.notes:
            logger.info(_("importcsvsummary.error.details"))
            for note in detail_notes:
                text = note.get("text") or note.get("value") or ""
                logger.info(f"  {note.get('type', '?')}: {text}")
            for text in job_done.notes or []:
                logger.info(f"  {text}")
