import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from chalicelib.service.constant_brand.service import AsyncConstantBrandService
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
async def test_constant_brand_service(client, factory, invoker):
    # given
    service = AsyncConstantBrandService(command_factory=factory, invoker=invoker)
    # when & then
    result = await service.find_all()
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(r, ConstantBrandEntity) for r in result)
