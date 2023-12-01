import pytest

from chalicelib.persistant.refactor.factory import AsyncMongoFactory


@pytest.fixture(scope="module")
def factory(client):
    return AsyncMongoFactory(client=client)
