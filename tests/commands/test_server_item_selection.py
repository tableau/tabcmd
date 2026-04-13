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


def test_nested_projects_same_leaf_name_returns_correct_datasource_per_container():
    logger = _Logger()
    # Simulate three separate 'Cats' projects that exist at different levels:
    # MyProjects/ProjectA/Cats, MyProjects/ProjectB/Cats, and MyProjects/Cats
    cats_under_project_a = _ProjectItem(project_id="cats-A", name="Cats")
    cats_under_project_b = _ProjectItem(project_id="cats-B", name="Cats")
    cats_under_root = _ProjectItem(project_id="cats-root", name="Cats")

    # Three datasources all named identically but owned by different 'Cats' projects
    items = [
        _DummyItem(name="my-datasource", project_id="cats-A"),
        _DummyItem(name="my-datasource", project_id="cats-B"),
        _DummyItem(name="my-datasource", project_id="cats-root"),
    ]
    endpoint = _DatasourcesEndpoint(items)

    # Each lookup should return exactly one item from the target project id
    res_a = Server.get_items_by_name(logger, endpoint, "my-datasource", cats_under_project_a)
    assert len(res_a) == 1 and res_a[0].project_id == "cats-A"

    res_b = Server.get_items_by_name(logger, endpoint, "my-datasource", cats_under_project_b)
    assert len(res_b) == 1 and res_b[0].project_id == "cats-B"

    res_root = Server.get_items_by_name(logger, endpoint, "my-datasource", cats_under_root)
    assert len(res_root) == 1 and res_root[0].project_id == "cats-root"
