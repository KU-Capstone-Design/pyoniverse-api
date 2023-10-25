from chalicelib.common.model.api import ApiSchema
from chalicelib.domain.brand.model.brand_response import BrandDetailResponseSchema
from tests.mock.mock import env, test_client


def test_spec_brand(env, test_client):
    import json

    res = test_client.http.get("/v1/brand/cu")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert ApiSchema.get_schema(BrandDetailResponseSchema).validate(body) == {}
