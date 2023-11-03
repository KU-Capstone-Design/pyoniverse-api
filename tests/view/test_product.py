from chalicelib.business.product.dto.response import ProductResponseDto
from chalicelib.view.model.api import Api
from tests.mock.mock import env, injector, test_client
from tests.schema.product.product_response import ProductResponseSchema


def test_spec_product_detail(env, test_client, injector):
    import json

    res = test_client.http.get("/v1/product/1")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(ProductResponseSchema, body, many=False) == {}
