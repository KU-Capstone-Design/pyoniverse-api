import pytest

from chalicelib.extern.dependency_injector.injector import MainInjector
from chalicelib.view.model.api import Api
from tests.mock.mock import env, test_client
from tests.schema.search.search_home_response import SearchHomeResponseSchema


@pytest.fixture
def injector(env):
    injector = MainInjector()
    injector.inject()


def test_spec_search_home(env, test_client, injector):
    import json

    res = test_client.http.get("/v1/search")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(SearchHomeResponseSchema, body, many=False) == {}
