import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.persistant.asyncio.mongo.command import AsyncMongoEqualCommand
from chalicelib.persistant.asyncio.mongo.command_factory import AsyncMongoCommandFactory
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


def test_factory(client):
    # given
    factory = AsyncMongoCommandFactory(client)
    # when
    command = factory.get_equal_command(
        db_name="constant", rel_name="test_rel", key="test_key", value="test_value"
    )
    # then
    assert isinstance(command, AsyncMongoEqualCommand)
