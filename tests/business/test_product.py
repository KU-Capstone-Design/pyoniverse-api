import os
from asyncio import AbstractEventLoop

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.business.product.business import AsyncProductBusiness
from chalicelib.business.product.dto.request import ProductRequestDto
from chalicelib.business.product.dto.response import ProductResponseDto
from chalicelib.converter.product import ProductConverter
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.mongo.command_factory import AsyncMongoCommandFactory
from chalicelib.service.constant_brand.service import AsyncConstantBrandService
from chalicelib.service.product.service import AsyncProductService
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


@pytest.fixture
def loop(client) -> AbstractEventLoop:
    return client.get_io_loop()


@pytest.fixture
def factory(client):
    return AsyncMongoCommandFactory(client)


@pytest.fixture
def product_service(factory):
    return AsyncProductService(command_factory=factory, invoker=AsyncInvoker())


@pytest.fixture
def constant_brand_service(factory):
    return AsyncConstantBrandService(command_factory=factory, invoker=AsyncInvoker())


def test_product_business(product_service, constant_brand_service, loop):
    # given
    business = AsyncProductBusiness(
        product_service=product_service,
        constant_brand_service=constant_brand_service,
        converter=ProductConverter(),
        loop=loop,
    )
    # when
    response: ProductResponseDto = business.get_detail(request=ProductRequestDto(id=1))
    # then
    assert isinstance(response, ProductResponseDto)
    assert response.best_brand in {b.id for b in response.brands}
