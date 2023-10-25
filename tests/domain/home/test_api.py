from chalicelib.common.model.api import Api
from chalicelib.domain.home.model.event_response import HomeEventResponseSchema
from chalicelib.domain.home.model.product_response import HomeProductResponseSchema
from chalicelib.domain.home.model.store_response import HomeStoreResponseSchema
from tests.mock.mock import env, test_client


def test_spec_products(env, test_client):
    import json

    res = test_client.http.get("/v1/home?type=products")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(HomeProductResponseSchema, body, many=False) == {}


def test_spec_events(env, test_client):
    import json

    res = test_client.http.get("/v1/home?type=events")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(HomeEventResponseSchema, body, many=False) == {}


def test_spec_brands(env, test_client):
    import json

    res = test_client.http.get("/v1/home")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(HomeStoreResponseSchema, body, many=False) == {}
