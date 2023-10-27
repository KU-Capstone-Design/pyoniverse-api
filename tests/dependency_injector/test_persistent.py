import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.dependency_injector.persistant import PersistentInjector
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.mongo.command_factory import AsyncMongoCommandFactory
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


def test_persistent_injector_without_dependency(client):
    # given
    injector = PersistentInjector()
    # when & then
    try:
        injector.check_dependencies()
    except Exception:
        assert True
    else:
        assert False


def test_persistent_injector(client):
    # given
    injector = PersistentInjector(client=client)
    # when & then
    assert isinstance(injector.command_factory(), AsyncMongoCommandFactory)
    assert isinstance(injector.invoker(), AsyncInvoker)
    assert injector.command_factory() is injector.command_factory()
    assert injector.invoker() is injector.invoker()
