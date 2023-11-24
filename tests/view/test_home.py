from chalicelib.view.model.api import Api
from tests.mock.mock import env, injector, test_client
from tests.schema.home.event_response import HomeEventResponseSchema
from tests.schema.home.product_response import HomeProductResponseSchema
from tests.schema.home.store_response import HomeStoreResponseSchema


def test_spec_products(env, test_client, injector):
    import json

    res = test_client.http.get("/v1/home?type=products")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(HomeProductResponseSchema, body, many=False) == {}


def test_spec_events(env, test_client, injector):
    import json

    res = test_client.http.get("/v1/home?type=events")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(HomeEventResponseSchema, body, many=False) == {}


def test_spec_brands(env, test_client, injector):
    import json

    res = test_client.http.get("/v1/home")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(HomeStoreResponseSchema, body, many=False) == {}
