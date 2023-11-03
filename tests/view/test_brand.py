import os
from asyncio import AbstractEventLoop

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.business.brand.business import AsyncBrandBusiness
from chalicelib.view.model.api import Api
from chalicelib.converter.brand import BrandConverter
from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from chalicelib.service.brand.service import AsyncBrandService
from chalicelib.view.brand_view import BrandView
from tests.mock.mock import env, test_client
from tests.schema.brand.brand_response import BrandDetailResponseSchema


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
def invoker():
    return AsyncInvoker()


@pytest.fixture
def brand_service(factory, invoker):
    return AsyncBrandService(command_factory=factory, invoker=invoker)


@pytest.fixture
def brand_business(brand_service, loop):
    return AsyncBrandBusiness(
        brand_service=brand_service, loop=loop, converter=BrandConverter()
    )


def test_spec_brand(env, test_client, brand_business):
    import json

    BrandView.business = brand_business
    res = test_client.http.get("/v1/brand/cu")
    body = json.loads(res.body)
    assert res.status_code == 200

    assert Api.validate(BrandDetailResponseSchema, body, many=False) == {}
