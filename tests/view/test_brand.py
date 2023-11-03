from chalicelib.view.model.api import Api
from tests.mock.mock import env, injector, test_client
from tests.schema.brand.brand_response import BrandDetailResponseSchema


def test_spec_brand(env, injector, test_client):
    import json

    res = test_client.http.get("/v1/brand/cu")
    body = json.loads(res.body)
    assert res.status_code == 200

    assert Api.validate(BrandDetailResponseSchema, body, many=False) == {}
