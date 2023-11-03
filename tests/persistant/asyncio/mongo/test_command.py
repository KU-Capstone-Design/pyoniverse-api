import os
from asyncio import AbstractEventLoop

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.persistant.asyncio.mongo.command import (
    AsyncMongoEqualCommand,
    AsyncMongoSortByLimit10Command,
)
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


def test_invalid_equal_command(client):
    # given
    rel_name = "error_rel_name"
    key, value = None, None
    # when & then
    try:
        AsyncMongoEqualCommand(
            client=client,
            rel_name=rel_name,
            key=key,
            value=value,
        )
    except AssertionError:
        assert True
    else:
        assert False

    try:
        AsyncMongoEqualCommand(
            client=client,
            rel_name=None,
            key="key",
            value=value,
        )
    except AssertionError:
        assert True
    else:
        assert False

    try:
        AsyncMongoEqualCommand(
            client=None,
            rel_name=rel_name,
            key="key",
            value=value,
        )
    except AssertionError:
        assert True
    else:
        assert False


def test_equal_command(client):
    # given
    rel_name = "brands"
    db_name = "constant"
    key = "id"
    value = 1
    # when
    command = AsyncMongoSortByLimit10Command(
        rel_name=rel_name, db_name=db_name, key=key, value=value, client=client
    )
    loop: AbstractEventLoop = client.get_io_loop()
    result = loop.run_until_complete(command.execute())
    # then
    assert len(result) <= 10
    assert sorted(result, key=lambda x: x.id) == result
