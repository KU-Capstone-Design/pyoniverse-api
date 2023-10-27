import os
from asyncio import AbstractEventLoop

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.business.brand.business import AsyncBrandBusiness
from chalicelib.business.brand.converter import BrandConverter
from chalicelib.business.brand.dto.request import BrandRequestDto
from chalicelib.business.brand.dto.response import BrandResponseDto
from chalicelib.entity.brand import BrandEntity
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.mongo.command_factory import AsyncMongoCommandFactory
from chalicelib.service.brand.service import AsyncBrandService
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
def brand_service(factory, invoker):
    return AsyncBrandService(command_factory=factory, invoker=invoker)


def test_brand_business(brand_service, loop):
    # given
    business = AsyncBrandBusiness(
        brand_service=brand_service, converter=BrandConverter(), loop=loop
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
