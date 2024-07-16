import argparse
import io

import tableauserverclient as TSC
from typing import NamedTuple, TextIO, Union
from unittest.mock import *


def create_fake_item():
    fake_item = MagicMock()
    fake_item.name = "fake-name"
    fake_item.id = "fake-id"
    fake_item.pdf = b"/pdf-representation-of-view"
    fake_item.extract_encryption_mode = "Disabled"
    return fake_item

def create_fake_job():
    fake_job = MagicMock()
    fake_job.id = "fake-job-id"
    return fake_job

def set_up_mock_args():
    mock_args = argparse.Namespace()
    # auth/connection values
    mock_args.timeout = None
    mock_args.username = None
    mock_args.server = None
    mock_args.password_file = None
    mock_args.token_file = None
    mock_args.token_name = None
    mock_args.token_value = None
    mock_args.no_prompt = False
    mock_args.certificate = None
    mock_args.no_certcheck = True
    mock_args.no_proxy = True
    mock_args.proxy = None
    mock_args.password = None
    mock_args.site_name = None

    # these are just really common
    mock_args.project_name = None
    mock_args.parent_project_path = None
    mock_args.parent_path = None
    mock_args.continue_if_exists = False    
    mock_args.recursive = False
    mock_args.logging_level="DEBUG"
    return mock_args


# TODO: get typings for argparse
class NamedObject(NamedTuple):
    name: str
ArgparseFile = Union[TextIO, NamedObject]

def set_up_mock_file(content=["Test", "", "Test", ""]) -> ArgparseFile:
    # the empty string represents EOF
    # the tests run through the file twice, first to validate then to fetch
    mock = MagicMock(io.TextIOWrapper)
    mock.readline.side_effect = content
    mock.name = "file-mock"
    return mock

def set_up_mock_path(mock_path):
    mock_path.exists = lambda x: True
    mock_path.isfile = lambda x: True
    mock_path.isdir = lambda x: True 
    mock_path.splitext = lambda x: ['file', 'twbx']
    mock_path.join = lambda x, y: x + "/" + y
    mock_path.basename = lambda x: str(x)
    return mock_path


def set_up_mock_server(mock_session):
    
    mock_session.return_value = mock_session
    mock_server = MagicMock(TSC.Server, autospec=True)
    getter = MagicMock()
    # basically we want to mock out everything in TSC 
    getter.get = MagicMock("get anything", return_value=([create_fake_item()], 1))
    getter.publish = MagicMock("publish", return_value=create_fake_item())

    mock_server.any_item_type = getter
    mock_server.flows = getter
    mock_server.groups = getter
    mock_server.projects = getter
    mock_server.sites = getter
    mock_server.users = getter
    mock_server.views = getter
    mock_server.workbooks = getter
    
    fake_job = create_fake_job()
    # ideally I would only set these on the specific objects that have each action, but this is a start
    getter.create_extract = MagicMock("create_extract", return_value=fake_job)
    getter.decrypt_extract = MagicMock("decrypt_extract", return_value=fake_job)
    getter.delete_extract = MagicMock("delete_extract", return_value=fake_job)
    getter.encrypt_extracts = MagicMock("encrypt_extracts", return_value=fake_job)
    getter.reencrypt_extract = MagicMock("reencrypt_extract", return_value=fake_job)
    getter.refresh = MagicMock("refresh", return_value=fake_job)
    
    # for test access
    mock_session.internal_server = mock_server
    mock_session.create_session.return_value = mock_server

    return mock_session
