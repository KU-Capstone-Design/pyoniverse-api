from chalicelib.domain.home.model.event_response import HomeEventResponseSchema
from chalicelib.domain.home.model.product_response import HomeProductResponseSchema
from chalicelib.domain.home.model.store_response import HomeStoreResponseSchema
from chalicelib.common.model.api import ApiSchema
from tests.mock.mock import test_client, env, headers


def test_spec_products(env, test_client, headers):
    import json
    import gzip

    res = test_client.http.get("/v1/home?type=products", headers=headers)
    body = json.loads(gzip.decompress(res.body).decode("utf-8"))
    assert res.status_code == 200
    assert ApiSchema.get_schema(HomeProductResponseSchema).validate(body) == {}


def test_spec_events(env, test_client, headers):
    import json
    import gzip

    res = test_client.http.get("/v1/home?type=events", headers=headers)
    body = json.loads(gzip.decompress(res.body).decode("utf-8"))
    assert res.status_code == 200
    assert ApiSchema.get_schema(HomeEventResponseSchema).validate(body) == {}


def test_spec_brands(env, test_client, headers):
    import json
    import gzip

    res = test_client.http.get("/v1/home", headers=headers)
    body = json.loads(gzip.decompress(res.body).decode("utf-8"))
    assert res.status_code == 200
    assert ApiSchema.get_schema(HomeStoreResponseSchema).validate(body) == {}
