import argparse
import unittest
from unittest import mock

from tabcmd.commands.extracts.refresh_extracts_command import RefreshExtracts


def _sync_args(**overrides):
    ns = argparse.Namespace(
        logging_level="INFO",
        datasource="ds",
        workbook=None,
        project_name=None,
        parent_project_path=None,
        addcalculations=False,
        removecalculations=False,
        incremental=False,
        synchronous=True,
        timeout=None,
    )
    for key, value in overrides.items():
        setattr(ns, key, value)
    return ns


@mock.patch("tabcmd.commands.extracts.refresh_extracts_command.Extracts.get_wb_or_ds_for_extracts")
@mock.patch("tabcmd.commands.auth.session.Session.create_session")
class RefreshExtractsTimeoutTest(unittest.TestCase):
    def _run(self, mock_session, args):
        server = mock.MagicMock()
        mock_session.return_value = server
        RefreshExtracts.run_command(args)
        return server

    def test_timeout_is_passed_as_number(self, mock_session, mock_get_item):
        server = self._run(mock_session, _sync_args(timeout="60"))
        job = server.datasources.refresh.return_value
        server.jobs.wait_for_job.assert_called_once_with(job_id=job, timeout=60)

    def test_missing_timeout_waits_indefinitely(self, mock_session, mock_get_item):
        server = self._run(mock_session, _sync_args(timeout=None))
        job = server.datasources.refresh.return_value
        server.jobs.wait_for_job.assert_called_once_with(job_id=job, timeout=None)
