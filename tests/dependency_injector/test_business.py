import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.business.brand.business import AsyncBrandBusiness
from chalicelib.converter.brand import BrandConverter
from chalicelib.converter.event import EventConverter
from chalicelib.converter.home import HomeConverter
from chalicelib.converter.metric import MetricConverter
from chalicelib.converter.product import ProductConverter
from chalicelib.converter.search import SearchConverter
from chalicelib.extern.dependency_injector.business import BusinessInjector
from chalicelib.extern.dependency_injector.persistant import PersistentInjector
from chalicelib.extern.dependency_injector.service import ServiceInjector
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


@pytest.fixture
def persistent_injector(client):
    return PersistentInjector(client=client)


@pytest.fixture
def service_injector(persistent_injector):
    injector = ServiceInjector(
        command_factory=persistent_injector.command_factory(),
        brand_invoker=persistent_injector.invoker(),
        constant_brand_invoker=persistent_injector.invoker(),
        product_invoker=persistent_injector.invoker(),
        event_invoker=persistent_injector.invoker(),
    )
    return injector


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
        constant_brand_service=service_injector.constant_brand_service(),
        event_service=service_injector.event_service(),
        product_service=service_injector.product_service(),
        brand_converter=BrandConverter(),
        home_converter=HomeConverter(),
        event_converter=EventConverter(),
        search_converter=SearchConverter(),
        product_converter=ProductConverter(),
        metric_converter=MetricConverter(),
        loop=loop,
    )
    # when & then
    assert isinstance(injector.brand_business(), AsyncBrandBusiness)
    assert injector.brand_business() is injector.brand_business()
