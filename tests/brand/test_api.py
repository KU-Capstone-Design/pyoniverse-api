from chalicelib.domain.brand.model.brand_response import BrandDetailResponseSchema
from chalicelib.model.api import ApiSchema
from tests.mock.mock import test_client, env, headers


def test_spec_brand(env, test_client, headers):
    import json
    import gzip

    res = test_client.http.get("/v1/brand/cu", headers=headers)
    body = json.loads(gzip.decompress(res.body).decode("utf-8"))
    assert res.status_code == 200
    assert ApiSchema.get_schema(BrandDetailResponseSchema).validate(body) == {}
