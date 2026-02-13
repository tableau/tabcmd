import pytest
import tableauserverclient as TSC

from tabcmd.commands.server import Server


class _Logger:
    def debug(self, *_args, **_kwargs):
        pass


class _DummyItem:
    def __init__(self, name: str, project_id: str):
        self.name = name
        self.project_id = project_id


class _DummyPagination:
    def __init__(self, total_available: int, page_number: int = 1, page_size: int = 100):
        self.total_available = total_available
        self.page_number = page_number
        self.page_size = page_size


class _DatasourcesEndpoint:
    # Deliberately named so type(item_endpoint).__name__ == "Datasources"
    def __init__(self, items):
        self._items = items

    def get(self, _req_option: TSC.RequestOptions):
        # Ignore server-side filters for this unit test; we validate client-side disambiguation
        return self._items, _DummyPagination(total_available=len(self._items))


class _ProjectItem:
    # Minimal project-like object carrying id/name used by Server.get_items_by_name
    def __init__(self, project_id: str, name: str):
        self.id = project_id
        self.name = name


def test_filters_datasources_by_exact_project_id_when_container_provided():
    logger = _Logger()
    container = _ProjectItem(project_id="proj-A", name="Shared")
    # Two datasources with identical names, different project ownership
    items = [
        _DummyItem(name="Sales", project_id="proj-A"),
        _DummyItem(name="Sales", project_id="proj-B"),
    ]
    endpoint = _DatasourcesEndpoint(items)

    results = Server.get_items_by_name(logger, endpoint, "Sales", container)

    assert len(results) == 1
    assert results[0].project_id == "proj-A"


def test_raises_not_found_when_no_items_match_container_after_disambiguation():
    logger = _Logger()
    container = _ProjectItem(project_id="proj-Z", name="Shared")
    items = [
        _DummyItem(name="Sales", project_id="proj-A"),
        _DummyItem(name="Sales", project_id="proj-B"),
    ]
    endpoint = _DatasourcesEndpoint(items)

    with pytest.raises(TSC.ServerResponseError):
        Server.get_items_by_name(logger, endpoint, "Sales", container)
