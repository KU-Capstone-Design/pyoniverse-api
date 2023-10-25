from chalicelib.common.model.api import Api
from chalicelib.domain.brand.model.brand_response import BrandDetailResponseSchema
from tests.mock.mock import env, test_client


def test_spec_brand(env, test_client):
    import json

    res = test_client.http.get("/v1/brand/cu")
    body = json.loads(res.body)
    assert res.status_code == 200

    assert Api.validate(BrandDetailResponseSchema, body, many=False) == {}
