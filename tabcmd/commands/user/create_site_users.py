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
        args_group.add_argument("--errors-file", default=None, help=_("createsiteusers.options.errors-file"))

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
        except Exception as e:
            # includes ServerResponseError and version-gate errors on servers without bulk_add
            Errors.exit_with_error(logger, exception=e)
            return

        # Under --nowait the job id is the only way to track the import, so show it even when silent.
        if args.nowait or not args.silent_progress:
            logger.info(_("importcsvsummary.job.queued").format(job.id))

        if args.nowait:
            # Fire and forget. Server processes the job asynchronously; caller
            # can query with `tabcmd get job/<id>` or via the REST API.
            return

        # Wait for the server-side job to finish. Under --silent-progress the
        # framework's own debug logging is still emitted but we skip our own
        # per-completion summary.
        try:
            job_done = server.jobs.wait_for_job(job_id=job.id, timeout=cls._timeout_seconds(args.timeout))
        except JobFailedException as je:
            # JobFailedException only carries the legacy job.notes, which can be empty
            # even when status_notes names the rejected row and reason.
            cls._report_job_details(logger, je.job, logger.error, args.silent_progress, args.errors_file)
            Errors.exit_with_error(logger, exception=je)
            return
        except TimeoutError as te:
            # the import keeps running server-side; say so and give the id so it isn't blindly retried
            logger.error(_("importcsvsummary.job.timeout").format(job.id))
            Errors.exit_with_error(logger, exception=te)
            return
        except Exception as e:
            Errors.exit_with_error(logger, exception=e)
            return

        if args.silent_progress:
            # No console summary, but rejected rows must not vanish: save them to a file.
            cls._report_job_details(logger, job_done, logger.info, True, args.errors_file)
            return

        # Summarize per-row outcomes. `status_notes` is populated for
        # UserImport jobs; each entry is a dict with keys type/value/text.
        # The specific types the server emits are documented at
        # https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_jobs_tasks_and_schedules.htm#query_job
        # (CountOfUsersAddedToSite, CountOfUsersSkipped, etc.).
        status_notes = job_done.status_notes or []
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

        cls._report_job_details(logger, job_done, logger.info, False, args.errors_file)

    @staticmethod
    def _timeout_seconds(timeout):
        """--timeout arrives as a string; wait_for_job compares it with elapsed seconds."""
        try:
            seconds = int(timeout)
        except (TypeError, ValueError):
            return None
        return seconds if seconds > 0 else None

    @staticmethod
    def _job_detail_lines(job):
        """Per-row messages for a finished job: any statusNote whose type isn't a CountOf* aggregate, plus legacy notes."""
        status_notes = getattr(job, "status_notes", None) or []
        detail_notes = [n for n in status_notes if not (n.get("type") or "").startswith("CountOf")]
        lines = []
        for note in detail_notes:
            text = note.get("text") or note.get("value") or ""
            lines.append(f"{note.get('type', '?')}: {text}")
        lines.extend(str(text) for text in getattr(job, "notes", None) or [])
        return lines

    @classmethod
    def _report_job_details(cls, logger, job, log_line, silent, errors_file=None):
        lines = cls._job_detail_lines(job)
        if not lines:
            return
        if silent or errors_file:
            path = errors_file or f"createsiteusers-errors-{job.id}.txt"
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines) + "\n")
                logger.error(_("importcsvsummary.error.file").format(path))
                return
            except OSError:
                pass  # can't write the file: fall through and show the details instead
        log_line(_("importcsvsummary.error.details"))
        for line in lines:
            log_line(f"  {line}")
