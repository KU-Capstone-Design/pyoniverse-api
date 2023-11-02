import os
from asyncio import AbstractEventLoop

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.business.metric.business import AsyncMetricBusiness
from chalicelib.business.metric.model.request import MetricRequestDto
from chalicelib.business.metric.model.response import MetricResponseDto
from chalicelib.business.product.business import AsyncProductBusiness
from chalicelib.business.product.dto.request import ProductRequestDto
from chalicelib.business.product.dto.response import ProductResponseDto
from chalicelib.converter.metric import MetricConverter
from chalicelib.converter.product import ProductConverter
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.mongo.command_factory import AsyncMongoCommandFactory
from chalicelib.service.event.service import AsyncEventService
from chalicelib.service.product.service import AsyncProductService
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


@pytest.fixture
def loop(client) -> AbstractEventLoop:
    return client.get_io_loop()


@pytest.fixture
def factory(client):
    return AsyncMongoCommandFactory(client)


@pytest.fixture
def product_service(factory):
    return AsyncProductService(command_factory=factory, invoker=AsyncInvoker())


@pytest.fixture
def event_service(factory):
    return AsyncEventService(command_factory=factory, invoker=AsyncInvoker())


def test_product_business_get_good_count(product_service, event_service, loop):
    # given
    business = AsyncMetricBusiness(
        product_service=product_service,
        event_service=event_service,
        converter=MetricConverter(),
        loop=loop,
    )
    request1 = MetricRequestDto(id=1, domain="product")
    request2 = MetricRequestDto(id=1, domain="event")
    invalid_request = MetricRequestDto(id=1, domain="invalid")
    # when
    response1: MetricResponseDto = business.get_good_count(request1)
    response2: MetricResponseDto = business.get_good_count(request2)
    # then
    assert isinstance(response1, MetricResponseDto) and isinstance(
        response2, MetricResponseDto
    )
    assert (
        response1.id == request1.id
        and response1.domain == request1.domain
        and isinstance(response1.value, int)
    )
    assert (
        response2.id == request2.id
        and response2.domain == request2.domain
        and isinstance(response2.value, int)
    )

    try:
        business.get_good_count(invalid_request)
        assert False
    except Exception:
        assert True


def test_product_business_get_view_count(product_service, event_service, loop):
    # given
    business = AsyncMetricBusiness(
        product_service=product_service,
        event_service=event_service,
        converter=MetricConverter(),
        loop=loop,
    )
    request1 = MetricRequestDto(id=1, domain="product")
    request2 = MetricRequestDto(id=1, domain="event")
    invalid_request = MetricRequestDto(id=1, domain="invalid")
    # when
    response1: MetricResponseDto = business.get_view_count(request1)
    response2: MetricResponseDto = business.get_view_count(request2)
    # then
    assert isinstance(response1, MetricResponseDto) and isinstance(
        response2, MetricResponseDto
    )
    assert (
        response1.id == request1.id
        and response1.domain == request1.domain
        and isinstance(response1.value, int)
    )
    assert (
        response2.id == request2.id
        and response2.domain == request2.domain
        and isinstance(response2.value, int)
    )

    try:
        business.get_view_count(invalid_request)
        assert False
    except Exception:
        assert True
