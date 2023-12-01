import pytest

from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from chalicelib.persistant.asyncio.invoker import AsyncInvoker


@pytest.fixture(scope="package")
def factory(client):
    return AsyncCommandFactory(client)


@pytest.fixture(scope="function")
def invoker():
    return AsyncInvoker()
