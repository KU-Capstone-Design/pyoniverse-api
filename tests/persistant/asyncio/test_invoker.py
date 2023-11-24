import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.entity.product import ProductEntity
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


@pytest.fixture
def factory(client):
    return AsyncCommandFactory(client)


def test_invoker(client, factory):
    # given
    invoker = AsyncInvoker()
    invoker.add_command(
        factory.get_equal_command(
            db_name="constant", rel_name="brands", key="id", value=1
        )
    )
    invoker.add_command(
        factory.get_equal_command(
            db_name="service", rel_name="products", key="id", value=1
        )
    )
    # when
    result = client.get_io_loop().run_until_complete(invoker.invoke())
    # then
    assert isinstance(result[0], ConstantBrandEntity)
    assert isinstance(result[1], ProductEntity)
    try:
        # invoker는 비워진다.
        invoker.pop_command()
    except IndexError:
        assert True
    else:
        assert False
