from chalicelib.view.model.api import Api
from tests.schema.product.product_response import ProductResponseSchema


def test_spec_product_detail(env, test_client, event_loop):
    import json

    res = test_client.http.get("/v1/product/1")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(ProductResponseSchema, body, many=False) == {}
