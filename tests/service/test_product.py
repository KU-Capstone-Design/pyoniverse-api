import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.entity.event import EventEntity
from chalicelib.entity.product import ProductEntity
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.mongo.command_factory import AsyncMongoCommandFactory
from chalicelib.service.product.service import AsyncProductService
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


def test_product_service(client, factory, invoker):
    # given
    service = AsyncProductService(command_factory=factory, invoker=invoker)
    loop = client.get_io_loop()
    chunk_size = 2
    # when & then
    result = loop.run_until_complete(
        service.find_chunk(
            sort_key="good_count", direction="desc", chunk_size=chunk_size
        )
    )
    assert isinstance(result, list)
    assert 0 < len(result) <= 2
    assert all(isinstance(r, ProductEntity) for r in result)
    assert sorted(result, key=lambda x: x.good_count, reverse=True) == result
