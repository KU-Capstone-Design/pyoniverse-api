import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.dependency_injector.persistant import PersistentInjector
from chalicelib.dependency_injector.tmp_service import ServiceInjector
from chalicelib.service.brand.service import AsyncBrandService
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


@pytest.fixture
def persistent_injector(client):
    return PersistentInjector(client=client)


def test_service_injector_without_dependency(persistent_injector):
    # given
    injector = ServiceInjector()
    # when & then
    try:
        injector.check_dependencies()
    except Exception:
        assert True
    else:
        assert False


def test_service_injector(persistent_injector):
    # given
    injector = ServiceInjector(
        command_factory=persistent_injector.command_factory(),
        brand_invoker=persistent_injector.invoker(),
        constant_brand_invoker=persistent_injector.invoker(),
        product_invoker=persistent_injector.invoker(),
        event_invoker=persistent_injector.invoker(),
    )
    # when & then
    assert isinstance(injector.brand_service(), AsyncBrandService)
    assert injector.brand_service() is injector.brand_service()
