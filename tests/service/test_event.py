import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.entity.event import EventEntity
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
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
