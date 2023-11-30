from chalicelib.view.model.api import Api
from tests.mock.mock import env, test_client, injector
from tests.schema.brand.brand_response import BrandDetailResponseSchema


def test_spec_brand(env, test_client, injector):
    import json

    res = test_client.http.get("/v1/brand/cu")
    body = json.loads(res.body)
    assert res.status_code == 200

    assert Api.validate(BrandDetailResponseSchema, body, many=False) == {}
