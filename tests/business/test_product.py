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
def invoker():
    return AsyncInvoker()


@pytest.fixture
def product_service(factory, invoker):
    return AsyncProductService(command_factory=factory, invoker=invoker)


def test_product_business(product_service, loop):
    # given
    business = AsyncProductBusiness(
        product_service=product_service,
        converter=ProductConverter(),
        loop=loop,
    )
    # when
    response = business.get_detail(request=ProductRequestDto(id=1))
    # then
    assert isinstance(response, ProductResponseDto)
