import os
from asyncio import gather

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.entity.product import ProductEntity
from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.service.product.service import AsyncProductService
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


def test_product_service_find_chunk(client, factory, invoker):
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


def test_product_service_find_one(client, factory, invoker):
    # given
    service = AsyncProductService(command_factory=factory, invoker=invoker)
    loop = client.get_io_loop()
    entity = ProductEntity(id=1)
    # when & then
    result = loop.run_until_complete(service.find_one(entity))
    assert isinstance(result, ProductEntity)
    assert result.id == entity.id


def test_product_service_add_values(client, factory, invoker):
    # given
    service = AsyncProductService(command_factory=factory, invoker=invoker)
    loop = client.get_io_loop()
    entity = ProductEntity(id=1, good_count=1, view_count=2)
    # when
    prv_entity: ProductEntity = loop.run_until_complete(service.find_one(entity))
    result: ProductEntity = loop.run_until_complete(service.add_values(entity))
    # then
    assert isinstance(result, ProductEntity)
    assert result.id == entity.id
    assert result.good_count == prv_entity.good_count + entity.good_count
    assert result.view_count == prv_entity.view_count + entity.view_count
