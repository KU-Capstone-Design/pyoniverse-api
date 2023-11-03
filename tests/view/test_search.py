from chalicelib.view.model.api import Api
from tests.mock.mock import env, injector, test_client
from tests.schema.search.search_home_response import SearchHomeResponseSchema
from tests.schema.search.search_result_response import SearchResultResponseSchema


def test_spec_search_home(env, test_client, injector):
    import json

    res = test_client.http.get("/v1/search")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(SearchHomeResponseSchema, body, many=False) == {}


def test_spec_search_result(env, test_client, injector):
    import json

    res = test_client.http.get("/v1/search/result?query=test+query")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(SearchResultResponseSchema, body, many=False) == {}
