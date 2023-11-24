import os
from asyncio import AbstractEventLoop

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.business.search.business import AsyncSearchBusiness
from chalicelib.business.search.dto.request import SearchResultRequestDto
from chalicelib.business.search.dto.response import (
    SearchHomeResponseDto,
    SearchResultResponseDto,
)
from chalicelib.converter.search import SearchConverter
from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.service.constant_brand.service import AsyncConstantBrandService
from chalicelib.service.product.service import AsyncProductService
from chalicelib.service.search.service import AsyncSearchService
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


@pytest.fixture
def loop(client) -> AbstractEventLoop:
    return client.get_io_loop()


@pytest.fixture
def factory(client):
    return AsyncCommandFactory(client)


@pytest.fixture
def constant_brand_service(factory):
    return AsyncConstantBrandService(command_factory=factory, invoker=AsyncInvoker())


@pytest.fixture
def product_service(factory):
    return AsyncProductService(command_factory=factory, invoker=AsyncInvoker())


@pytest.fixture
def search_service():
    return AsyncSearchService(engine_uri=os.getenv("SEARCH_ENGINE_URI"))


def test_search_business(constant_brand_service, product_service, search_service, loop):
    # given
    business = AsyncSearchBusiness(
        constant_brand_service=constant_brand_service,
        product_service=product_service,
        search_service=search_service,
        converter=SearchConverter(),
        loop=loop,
    )
    # when
    index = business.get_index()
    # then
    assert isinstance(index, SearchHomeResponseDto)


def test_search(constant_brand_service, product_service, search_service, loop):
    # given
    business = AsyncSearchBusiness(
        constant_brand_service=constant_brand_service,
        product_service=product_service,
        search_service=search_service,
        converter=SearchConverter(),
        loop=loop,
    )
    request = SearchResultRequestDto(
        query="우유",
    )
    # when
    res = business.get_result(request=request)
    # then
    assert isinstance(res, SearchResultResponseDto)
    for product in res.products:
        assert product.price != product.event_price
        if product.event_price is not None:
            assert product.event_price < product.price
    assert res.products_count == len(res.products)

    assert sorted(res.categories, key=lambda x: x.id) == res.categories
    assert sorted(res.brands, key=lambda x: x.id) == res.brands
    assert sorted(res.events, key=lambda x: x.id) == res.events
