import os

import pytest

from chalicelib.persistant.refactor.factory import AsyncMongoFactory
from chalicelib.service_refactor.constant_brand.service import AsyncConstantBrandService
from chalicelib.service_refactor.event.service import AsyncEventService
from chalicelib.service_refactor.product.service import AsyncProductService
from chalicelib.service_refactor.search.service import AsyncSearchService


@pytest.fixture(scope="module")
def factory(client):
    return AsyncMongoFactory(client)


@pytest.fixture(scope="module")
def constant_brand_service(factory):
    return AsyncConstantBrandService(factory=factory)


@pytest.fixture(scope="module")
def product_service(factory):
    return AsyncProductService(factory=factory)


@pytest.fixture(scope="module")
def event_service(factory):
    return AsyncEventService(factory=factory)


@pytest.fixture(scope="module")
def search_service():
    return AsyncSearchService(engine_uri=os.getenv("SEARCH_ENGINE_URI"))
