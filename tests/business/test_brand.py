import os
from asyncio import AbstractEventLoop

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.business.brand.business import AsyncBrandBusiness
from chalicelib.business.brand.dto.request import BrandRequestDto
from chalicelib.business.brand.dto.response import BrandResponseDto
from chalicelib.converter.brand import BrandConverter
from chalicelib.entity.brand import BrandEntity
from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
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
    return AsyncCommandFactory(client)


@pytest.fixture
def constant_brand_service(factory):
    return AsyncConstantBrandService(command_factory=factory, invoker=AsyncInvoker())


@pytest.fixture
def product_service(factory):
    return AsyncProductService(command_factory=factory, invoker=AsyncInvoker())


@pytest.fixture
def event_service(factory):
    return AsyncEventService(command_factory=factory, invoker=AsyncInvoker())


def test_brand_business(constant_brand_service, product_service, event_service, loop):
    # given
    business = AsyncBrandBusiness(
        constant_brand_service=constant_brand_service,
        product_service=product_service,
        event_service=event_service,
        converter=BrandConverter(),
        loop=loop,
    )
    # when
    result = business.get_detail_page(request=BrandRequestDto(slug="cu"))
    # then
    assert isinstance(result, BrandResponseDto)


def test_brand_converter():
    # given
    converter = BrandConverter()
    request = BrandRequestDto(slug="cu")
    # when & then
    entity = converter.convert_to_entity(request)
    assert isinstance(entity, BrandEntity) and entity.slug == request.slug

    response = converter.convert_to_dto(entity)
    assert isinstance(response, BrandResponseDto)
