import os
from typing import Sequence

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.entity.event import EventEntity
from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.service.event.service import AsyncEventService
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


def test_event_service(client, factory, invoker):
    # given
    service = AsyncEventService(command_factory=factory, invoker=invoker)
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
    assert all(isinstance(r, EventEntity) for r in result)
    assert sorted(result, key=lambda x: x.good_count, reverse=True) == result


def test_event_service_add_values(client, factory, invoker):
    # given
    service = AsyncEventService(command_factory=factory, invoker=invoker)
    loop = client.get_io_loop()
    entity = EventEntity(id=1, good_count=1, view_count=2)
    # when
    prv_entity: EventEntity = loop.run_until_complete(service.find_by_id(entity))
    result: EventEntity = loop.run_until_complete(service.add_values(entity))
    # then
    assert isinstance(result, EventEntity)
    assert result.id == entity.id
    assert result.good_count == prv_entity.good_count + entity.good_count
    assert result.view_count == prv_entity.view_count + entity.view_count


def test_event_find_chunk_by(client, factory, invoker):
    # given
    service = AsyncEventService(command_factory=factory, invoker=invoker)
    loop = client.get_io_loop()
    # when
    coroutine = service.find_chunk_by(
        filter_key="brand",
        filter_value=1,
        sort_key="good_count",
        direction="asc",
        chunk_size=3,
    )
    result: Sequence[EventEntity] = loop.run_until_complete(coroutine)
    assert isinstance(result, list)
