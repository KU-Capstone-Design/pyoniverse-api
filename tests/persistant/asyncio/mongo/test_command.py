import os
from asyncio import AbstractEventLoop

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.entity.product import ProductEntity
from chalicelib.persistant.asyncio.mongo.command import (
    AsyncMongoEqualCommand,
    AsyncMongoSelectBySortByCommand,
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


def test_select_by_sort_by_command(client):
    # given
    command = AsyncMongoSelectBySortByCommand(
        client=client,
        rel_name="products",
        db_name="service",
        key="brands.id",
        value=1,
        sort_key="good_count",
        sort_value="desc",
        chunk_size=3,
    )
    # when
    loop: AbstractEventLoop = client.get_io_loop()
    result = loop.run_until_complete(command.execute())
    # then
    assert len(result) <= 3
    assert sorted(result, key=lambda x: x.good_count, reverse=True) == result
    for r in result:
        p: ProductEntity = r
        ok = False
        for b in p.brands:
            if b.id == 1:
                ok = True
                break
        assert ok
