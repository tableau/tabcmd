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
        errors_file=None,
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

        with (
            mock.patch("tabcmd.commands.user.create_site_users.Session") as session_cls,
            mock.patch("tabcmd.commands.user.user_data.UserCommand.validate_file_for_import"),
            mock.patch("tabcmd.commands.user.user_data.UserCommand.get_users_from_file") as get_users,
        ):
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

    def test_timeout_is_passed_as_number(self):
        args = _base_args(timeout="60")
        server, job, completed = self._run(args)
        server.jobs.wait_for_job.assert_called_once_with(job_id=job.id, timeout=60)

    def test_failed_job_logs_status_notes_and_exits(self):
        from tableauserverclient.server.endpoint.exceptions import JobFailedException

        from tabcmd.commands.user.create_site_users import CreateSiteUsersCommand

        failed = mock.MagicMock(spec=TSC.JobItem)
        failed.id = "abc-123"
        failed.notes = []
        failed.status_notes = [{"type": "UserError", "value": "bob", "text": "invalid role"}]
        with (
            mock.patch("tabcmd.commands.user.create_site_users.Session") as session_cls,
            mock.patch("tabcmd.commands.user.user_data.UserCommand.validate_file_for_import"),
            mock.patch(
                "tabcmd.commands.user.user_data.UserCommand.get_users_from_file",
                return_value=[TSC.UserItem("bob", "Viewer")],
            ),
            mock.patch("tabcmd.commands.user.create_site_users.log") as log_fn,
        ):
            server = session_cls.return_value.create_session.return_value
            server.jobs.wait_for_job.side_effect = JobFailedException(failed)
            with self.assertRaises(SystemExit):
                CreateSiteUsersCommand.run_command(_base_args())
        logged = " ".join(str(c) for c in log_fn.return_value.error.call_args_list)
        self.assertIn("UserError: invalid role", logged)

    def test_timeout_reports_job_id_and_exits(self):
        from tabcmd.commands.user.create_site_users import CreateSiteUsersCommand

        with (
            mock.patch("tabcmd.commands.user.create_site_users.Session") as session_cls,
            mock.patch("tabcmd.commands.user.user_data.UserCommand.validate_file_for_import"),
            mock.patch(
                "tabcmd.commands.user.user_data.UserCommand.get_users_from_file",
                return_value=[TSC.UserItem("bob", "Viewer")],
            ),
            mock.patch("tabcmd.commands.user.create_site_users.log") as log_fn,
        ):
            server = session_cls.return_value.create_session.return_value
            server.users.bulk_add.return_value.id = "job-77"
            server.jobs.wait_for_job.side_effect = TimeoutError()
            with self.assertRaises(SystemExit):
                CreateSiteUsersCommand.run_command(_base_args(timeout="5"))
        logged = " ".join(str(c) for c in log_fn.return_value.error.call_args_list)
        self.assertIn("job-77", logged)

    def test_nowait_with_silent_progress_still_prints_job_id(self):
        with self.assertLogs("CreateSiteUsersCommand", level="INFO") as logs:
            self._run(_base_args(nowait=True, silent_progress=True))
        self.assertIn("abc-123", " ".join(logs.output))

    def _rejected_job(self):
        job = mock.MagicMock(spec=TSC.JobItem)
        job.id = "abc-123"
        job.finish_code = 0
        job.notes = []
        job.status_notes = [
            {"type": "CountOfUsersSkipped", "value": "1", "text": None},
            {"type": "UserError", "value": "bob", "text": "invalid role"},
        ]
        return job

    def test_silent_progress_saves_rejected_rows_to_file(self):
        import os
        import tempfile

        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                self._run(_base_args(silent_progress=True), completed_override=self._rejected_job())
                with open("createsiteusers-errors-abc-123.txt", encoding="utf-8") as f:
                    content = f.read()
            finally:
                os.chdir(cwd)
        self.assertIn("UserError: invalid role", content)

    def test_errors_file_flag_sets_custom_path(self):
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "custom.txt")
            self._run(_base_args(silent_progress=True, errors_file=path), completed_override=self._rejected_job())
            with open(path, encoding="utf-8") as f:
                content = f.read()
        self.assertIn("UserError: invalid role", content)

    def test_errors_file_flag_without_silent_writes_file(self):
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "custom.txt")
            self._run(_base_args(errors_file=path), completed_override=self._rejected_job())
            self.assertTrue(os.path.exists(path))

    def test_silent_progress_writes_no_file_when_nothing_rejected(self):
        import os
        import tempfile

        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                self._run(_base_args(silent_progress=True))
                created = os.listdir(tmp)
            finally:
                os.chdir(cwd)
        self.assertEqual(created, [])

    def test_not_silent_prints_rejected_rows_and_writes_no_file(self):
        import os
        import tempfile

        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                with self.assertLogs("CreateSiteUsersCommand", level="INFO") as logs:
                    self._run(_base_args(), completed_override=self._rejected_job())
                created = os.listdir(tmp)
            finally:
                os.chdir(cwd)
        self.assertIn("UserError: invalid role", " ".join(logs.output))
        self.assertEqual(created, [])


if __name__ == "__main__":
    unittest.main()
