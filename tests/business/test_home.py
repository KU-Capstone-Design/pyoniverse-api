import os
from asyncio import AbstractEventLoop

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.converter.brand import BrandConverter
from chalicelib.business.brand.dto.request import BrandRequestDto
from chalicelib.business.brand.dto.response import BrandResponseDto
from chalicelib.business.home.business import AsyncHomeBusiness
from chalicelib.converter.home import HomeConverter
from chalicelib.business.home.dto.request import HomeRequestDto
from chalicelib.business.home.dto.response import (
    HomeBrandsResponseDto,
    HomeEventsResponseDto,
    HomeProductsResponseDto,
)
from chalicelib.entity.brand import BrandEntity
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.mongo.command_factory import AsyncMongoCommandFactory
from chalicelib.service.constant_brand.service import AsyncConstantBrandService
from chalicelib.service.event.service import AsyncEventService
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
def event_service(factory, invoker):
    return AsyncEventService(command_factory=factory, invoker=invoker)


@pytest.fixture
def product_service(factory, invoker):
    return AsyncProductService(command_factory=factory, invoker=invoker)


def test_home_business(constant_brand_service, event_service, product_service, loop):
    # given
    business = AsyncHomeBusiness(
        constant_brand_service=constant_brand_service,
        event_service=event_service,
        product_service=product_service,
        converter=HomeConverter(),
        loop=loop,
    )
    # when
    events = business.get_list(request=HomeRequestDto(type="events"))
    products = business.get_list(request=HomeRequestDto(type="products"))
    stores = business.get_list(request=HomeRequestDto(type="stores"))
    # then
    assert isinstance(events, HomeEventsResponseDto)
    assert isinstance(products, HomeProductsResponseDto)
    assert isinstance(stores, HomeBrandsResponseDto)


def test_home_converter():
    # given
    converter = BrandConverter()
    request = BrandRequestDto(slug="cu")
    # when & then
    entity = converter.convert_to_entity(request)
    assert isinstance(entity, BrandEntity) and entity.slug == request.slug

    response = converter.convert_to_dto(entity)
    assert isinstance(response, BrandResponseDto)
