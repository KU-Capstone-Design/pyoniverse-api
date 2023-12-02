from contextlib import contextmanager

import pytest

from chalicelib.entity.product import ProductEntity
from chalicelib.persistant.factory import AsyncMongoFactory
from chalicelib.service.model.enum import OperatorEnum
from chalicelib.service.model.result import Result


@pytest.fixture
def factory(mongo_client):
    return AsyncMongoFactory(mongo_client)


@pytest.mark.asyncio
async def test_builder_find_one(factory):
    builder = factory.make("test", "products")

    # when
    builder.project("id")
    builder.project("name")
    builder.or_()
    builder.where(OperatorEnum.EQUAL, "id", 1)

    result: Result = await builder.read()
    entity = result.get()

    assert isinstance(entity, ProductEntity)
    assert entity.id == 1 and entity.name is not None


@pytest.mark.asyncio
async def test_builder_find_list(factory):
    builder = factory.make("test", "products")

    # when
    builder.project("price")
    builder.and_()
    builder.where(OperatorEnum.LESS_THAN, "price", 2000)

    result: Result = await builder.read()
    entities = result.get()

    assert isinstance(entities, list)
    for p in entities:
        assert p.price < 2000


@pytest.mark.asyncio
async def test_builder_find_complex(factory):
    builder = factory.make("test", "products")

    # when
    builder.project("price")
    builder.project("category")
    builder.project("brands")
    builder.and_()
    builder.where(OperatorEnum.LESS_THAN, "price", 3000)
    builder.where(OperatorEnum.IN, "category", [1, 2])
    builder.where(OperatorEnum.IN, "brands.id", [1, 2, 3])

    result: Result = await builder.read()
    entities = result.get()

    assert isinstance(entities, list)
    for p in entities:
        brands = {b.id for b in p.brands}
        assert p.price < 3000
        assert p.category in [1, 2]
        assert brands and brands.intersection({1, 2, 3})


@contextmanager
def not_raises():
    try:
        yield
    except Exception as e:
        assert False
    else:
        assert True


@pytest.mark.asyncio
async def test_builder_update(factory):
    builder = factory.make("test", "products")

    # when
    builder.and_()
    builder.where(OperatorEnum.EQUAL, "id", 10)

    with not_raises():
        result: Result = await builder.update(view_count=10, good_count=20)
        entity = result.get()
        assert entity.id == 10
