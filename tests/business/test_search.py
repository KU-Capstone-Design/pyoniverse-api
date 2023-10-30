import os
from asyncio import AbstractEventLoop

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.business.search.business import AsyncSearchBusiness
from chalicelib.business.search.dto.response import SearchHomeResponseDto
from chalicelib.converter.search import SearchConverter
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
def invoker():
    return AsyncInvoker()


@pytest.fixture
def constant_brand_service(factory, invoker):
    return AsyncConstantBrandService(command_factory=factory, invoker=invoker)


@pytest.fixture
def product_service(factory, invoker):
    return AsyncProductService(command_factory=factory, invoker=invoker)


def test_search_business(constant_brand_service, product_service, loop):
    # given
    business = AsyncSearchBusiness(
        constant_brand_service=constant_brand_service,
        product_service=product_service,
        converter=SearchConverter(),
        loop=loop,
    )
    # when
    index = business.get_index()
    # then
    assert isinstance(index, SearchHomeResponseDto)
