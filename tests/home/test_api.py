from chalicelib.common.model.api import ApiSchema
from chalicelib.domain.home.model.event_response import HomeEventResponseSchema
from chalicelib.domain.home.model.product_response import HomeProductResponseSchema
from chalicelib.domain.home.model.store_response import HomeStoreResponseSchema
from tests.mock.mock import env, test_client


def test_spec_products(env, test_client):
    import json

    res = test_client.http.get("/v1/home?type=products")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert ApiSchema.get_schema(HomeProductResponseSchema).validate(body) == {}


def test_spec_events(env, test_client):
    import json

    res = test_client.http.get("/v1/home?type=events")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert ApiSchema.get_schema(HomeEventResponseSchema).validate(body) == {}


def test_spec_brands(env, test_client):
    import json

    res = test_client.http.get("/v1/home")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert ApiSchema.get_schema(HomeStoreResponseSchema).validate(body) == {}
