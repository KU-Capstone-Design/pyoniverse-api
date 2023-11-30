import os

import pytest
from chalice import BadRequestError
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.entity.brand import BrandEntity
from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.service.brand.service import AsyncBrandService
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


@pytest.fixture
def factory(client):
    return AsyncCommandFactory(client)


@pytest.fixture
def invoker():
    return AsyncInvoker()


@pytest.mark.asyncio
async def test_brand_service(client, factory, invoker):
    # given
    service = AsyncBrandService(command_factory=factory, invoker=invoker)
    # when & then
    with pytest.raises(BadRequestError):
        await service.find_by_slug(None)

    result = await service.find_by_slug(BrandEntity(slug="cu"))
    assert isinstance(result, BrandEntity)
