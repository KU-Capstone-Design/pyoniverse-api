import os
from asyncio import AbstractEventLoop

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.business.event.business import AsyncEventBusiness
from chalicelib.converter.event import EventConverter
from chalicelib.business.event.dto.request import EventRequestDto
from chalicelib.business.event.dto.response import (
    EventDetailResponseDto,
    EventsResponseDto,
)
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from chalicelib.service.constant_brand.service import AsyncConstantBrandService
from chalicelib.service.event.service import AsyncEventService
from tests.mock.mock import env


@pytest.fixture
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


@pytest.fixture
def loop(client) -> AbstractEventLoop:
    return client.get_io_loop()


@pytest.fixture
def factory(client):
    return AsyncCommandFactory(client)


@pytest.fixture
def constant_brand_service(factory):
    return AsyncConstantBrandService(command_factory=factory, invoker=AsyncInvoker())


@pytest.fixture
def event_service(factory):
    return AsyncEventService(command_factory=factory, invoker=AsyncInvoker())


def test_event_business(constant_brand_service, event_service, loop):
    # given
    business = AsyncEventBusiness(
        constant_brand_service=constant_brand_service,
        event_service=event_service,
        converter=EventConverter(),
        loop=loop,
    )
    # when
    event_list_response = business.get_list(EventRequestDto(brand_slug="cu"))
    event_detail_response = business.get_detail(EventRequestDto(id=1))
    # then
    assert isinstance(event_list_response, EventsResponseDto)
    assert isinstance(event_detail_response, EventDetailResponseDto)
