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


def test_random_recommendation(env, test_client, injector):
    import json

    res1 = test_client.http.get("/v1/search")
    res2 = test_client.http.get("/v1/search")

    assert res1.status_code == 200 and res2.status_code == 200

    body1 = json.loads(res1.body)
    body2 = json.loads(res2.body)

    assert body1["data"]["recommendations"] != body2["data"]["recommendations"]


def test_spec_search_result(env, test_client, injector):
    import json

    res = test_client.http.get("/v1/search/result?query=우유")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(SearchResultResponseSchema, body, many=False) == {}


def test_spec_search_result_empty(env, test_client, injector):
    import json

    query = "이 검색어는 빈 배열을 반환합니다."
    res = test_client.http.get(f"/v1/search/result?query={query}")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(SearchResultResponseSchema, body, many=False) == {}
    assert len(body["data"]["products"]) == 0
