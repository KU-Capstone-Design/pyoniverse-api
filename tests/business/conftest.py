import os

import pytest

from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.service.constant_brand.service import AsyncConstantBrandService
from chalicelib.service.event.service import AsyncEventService
from chalicelib.service.product.service import AsyncProductService
from chalicelib.service.search.service import AsyncSearchService


@pytest.fixture(scope="module")
def factory(client):
    return AsyncCommandFactory(client)


@pytest.fixture(scope="module")
def constant_brand_service(factory):
    return AsyncConstantBrandService(command_factory=factory, invoker=AsyncInvoker())


@pytest.fixture(scope="module")
def product_service(factory):
    return AsyncProductService(command_factory=factory, invoker=AsyncInvoker())


@pytest.fixture(scope="module")
def event_service(factory):
    return AsyncEventService(command_factory=factory, invoker=AsyncInvoker())


@pytest.fixture(scope="module")
def search_service():
    return AsyncSearchService(engine_uri=os.getenv("SEARCH_ENGINE_URI"))
