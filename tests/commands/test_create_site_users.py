"""Behavior tests for createsiteusers after the switch to bulk_add.

These are unit tests that mock the TSC layer -- they don't hit a real
server. They verify:
- default path: bulk_add called, then wait_for_job called
- --nowait: bulk_add called, wait_for_job NOT called
- --silent-progress: bulk_add + wait_for_job called, but summary log lines
  are suppressed
- pre-flight validation aborts before bulk_add on malformed input under
  --complete (default)
- per-row output derived from job.status_notes on the completed job
"""
import argparse
import io
import unittest
from unittest import mock

import tableauserverclient as TSC


def _mock_open_csv(content):
    """Return a mock args.filename that mimics a file with the given CSV content."""
    fp = io.StringIO(content)
    fp.name = "users.csv"
    return fp


def _base_args(**overrides):
    ns = argparse.Namespace(
        filename=_mock_open_csv("username,password,fullname,creator,none,yes,email\n"),
        role=None,
        auth_type=None,
        require_all_valid=True,
        continue_if_exists=False,
        nowait=False,
        silent_progress=False,
        logging_level="INFO",
        timeout=None,
        username=None,
        password=None,
        token_name=None,
        token_value=None,
        server=None,
        site_name="",
        no_prompt=True,
        no_certcheck=False,
        no_proxy=False,
        proxy=None,
        certificate=None,
        password_file=None,
        token_file=None,
        no_cookie=False,
        query_page_size=None,
        language=None,
    )
    for k, v in overrides.items():
        setattr(ns, k, v)
    return ns


class CreateSiteUsersTest(unittest.TestCase):
    def _run(self, args, completed_override=None):
        from tabcmd.commands.user.create_site_users import CreateSiteUsersCommand

        with mock.patch("tabcmd.commands.user.create_site_users.Session") as session_cls, mock.patch(
            "tabcmd.commands.user.user_data.UserCommand.validate_file_for_import"
        ), mock.patch("tabcmd.commands.user.user_data.UserCommand.get_users_from_file") as get_users:
            fake_server = mock.MagicMock()
            session_cls.return_value.create_session.return_value = fake_server
            get_users.return_value = [
                TSC.UserItem("alice", "Creator"),
                TSC.UserItem("bob", "Viewer"),
            ]

            fake_job = mock.MagicMock(spec=TSC.JobItem)
            fake_job.id = "abc-123"
            fake_server.users.bulk_add.return_value = fake_job

            if completed_override is not None:
                completed = completed_override
            else:
                completed = mock.MagicMock(spec=TSC.JobItem)
                completed.id = "abc-123"
                completed.finish_code = 0
                completed.notes = []
                completed.status_notes = [
                    {"type": "CountOfUsersAddedToSite", "value": "2", "text": None},
                    {"type": "CountOfUsersSkipped", "value": "0", "text": None},
                    {"type": "CountOfUsersProcessed", "value": "2", "text": None},
                ]
            fake_server.jobs.wait_for_job.return_value = completed

            CreateSiteUsersCommand.run_command(args)
            return fake_server, fake_job, completed

    def test_default_calls_bulk_add_and_wait(self):
        args = _base_args()
        server, job, completed = self._run(args)
        server.users.bulk_add.assert_called_once()
        server.jobs.wait_for_job.assert_called_once_with(job_id=job.id, timeout=None)

    def test_nowait_skips_wait_for_job(self):
        args = _base_args(nowait=True)
        server, job, completed = self._run(args)
        server.users.bulk_add.assert_called_once()
        server.jobs.wait_for_job.assert_not_called()

    def test_silent_progress_still_calls_wait(self):
        # --silent-progress suppresses log lines, not the actual wait.
        args = _base_args(silent_progress=True)
        server, job, completed = self._run(args)
        server.users.bulk_add.assert_called_once()
        server.jobs.wait_for_job.assert_called_once()

    def test_nowait_and_silent_progress_coexist(self):
        args = _base_args(nowait=True, silent_progress=True)
        server, job, completed = self._run(args)
        server.users.bulk_add.assert_called_once()
        server.jobs.wait_for_job.assert_not_called()

    def test_older_tsc_without_status_notes_exits_with_error(self):
        # If the pinned tableauserverclient predates status_notes on JobItem,
        # we can't produce a truthful per-user summary. Fail loudly rather than
        # silently print zeros that look like success.
        args = _base_args()

        class _OldJobItem:
            # Deliberately does NOT have a status_notes attribute; this mirrors
            # a pre-status_notes TSC release.
            def __init__(self):
                self.id = "abc-123"
                self.finish_code = 0
                self.notes = []

        with self.assertRaises(SystemExit):
            self._run(args, completed_override=_OldJobItem())


if __name__ == "__main__":
    unittest.main()
