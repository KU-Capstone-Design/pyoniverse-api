import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.persistant.asyncio.mongo.command import (
    AsyncMongoEqualCommand,
    AsyncMongoSortByLimit10Command,
)
from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


def test_factory(client):
    # given
    factory = AsyncCommandFactory(client)
    # when
    eq_command = factory.get_equal_command(
        db_name="constant", rel_name="test_rel", key="test_key", value="test_value"
    )
    sort_by_limit_10_command = factory.get_sort_by_limit10_command(
        db_name="constant", rel_name="test_rel", key="test_key", value=1
    )
    # then
    assert isinstance(eq_command, AsyncMongoEqualCommand)
    assert isinstance(sort_by_limit_10_command, AsyncMongoSortByLimit10Command)
