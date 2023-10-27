import os

import pytest
from chalice import BadRequestError
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.entity.brand import BrandEntity
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.mongo.command_factory import AsyncMongoCommandFactory
from chalicelib.service.brand.service import AsyncBrandService
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


@pytest.fixture
def factory(client):
    return AsyncMongoCommandFactory(client)


@pytest.fixture
def invoker():
    return AsyncInvoker()


def test_brand_service(client, factory, invoker):
    # given
    service = AsyncBrandService(command_factory=factory, invoker=invoker)
    loop = client.get_io_loop()
    # when & then
    try:
        loop.run_until_complete(service.find_by_id(None))
    except BadRequestError:
        assert True
    else:
        assert False

    result = loop.run_until_complete(service.find_by_id(BrandEntity(id=1)))
    assert isinstance(result, BrandEntity)
