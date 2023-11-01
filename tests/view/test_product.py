import pytest

from chalicelib.business.product.dto.response import ProductResponseDto
from chalicelib.extern.dependency_injector.injector import MainInjector
from chalicelib.view.model.api import Api
from tests.mock.mock import env, test_client


@pytest.fixture
def injector(env):
    injector = MainInjector()
    injector.inject()


def test_spec_product_detail(env, test_client, injector):
    import json

    res = test_client.http.get("/v1/product/1")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(ProductResponseDto, body, many=False) == {}
