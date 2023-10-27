import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.business.brand.business import AsyncBrandBusiness
from chalicelib.business.brand.converter import BrandConverter
from chalicelib.dependency_injector.business import BusinessInjector
from chalicelib.dependency_injector.persistant import PersistentInjector
from chalicelib.dependency_injector.tmp_service import ServiceInjector
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


@pytest.fixture
def persistent_injector(client):
    return PersistentInjector(client=client)


@pytest.fixture
def service_injector(persistent_injector):
    return ServiceInjector(
        command_factory=persistent_injector.command_factory(),
        invoker=persistent_injector.invoker(),
    )


@pytest.fixture
def loop(client):
    return client.get_io_loop()


def test_business_injector_without_dependency(service_injector, loop):
    # given
    # when & then
    try:
        injector = BusinessInjector()
        injector.check_dependencies()
    except Exception:
        assert True
    else:
        assert False


def test_business_injector(service_injector, loop):
    # given
    injector = BusinessInjector(
        brand_service=service_injector.brand_service(),
        brand_converter=BrandConverter(),
        loop=loop,
    )
    # when & then
    assert isinstance(injector.brand_business(), AsyncBrandBusiness)
    assert injector.brand_business() is injector.brand_business()
