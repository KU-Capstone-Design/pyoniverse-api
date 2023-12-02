from typing import List

import pytest

from chalicelib.business.model.enum import OperatorEnum
from chalicelib.entity.product import ProductEntity
from chalicelib.service.product.service import AsyncProductService


@pytest.fixture
def service(factory):
    return AsyncProductService(factory=factory)


@pytest.mark.asyncio
async def test_product_service_find_chunk(service):
    # given
    chunk_size = 2
    # when & then
    result = await service.find_chunk(
        sort_key="good_count", direction="desc", chunk_size=chunk_size
    )
    assert isinstance(result, list)
    assert 0 < len(result) <= 2
    assert all(isinstance(r, ProductEntity) for r in result)
    assert sorted(result, key=lambda x: x.good_count, reverse=True) == result


@pytest.mark.asyncio
async def test_product_service_find_one(service):
    # given
    entity = ProductEntity(id=1)
    # when & then
    result = await service.find_one(entity)
    assert isinstance(result, ProductEntity)
    assert result.id == entity.id


@pytest.mark.asyncio
async def test_product_service_add_values(service):
    # given
    entity = ProductEntity(id=1, good_count=1, view_count=2)
    # when
    prv_entity: ProductEntity = await service.find_one(entity)
    result: ProductEntity = await service.add_values(entity)
    # then
    assert isinstance(result, ProductEntity)
    assert result.id == entity.id


@pytest.mark.asyncio
async def test_product_length(service):
    res = await service.get_length("status", 1)
    assert res > 0
    exactly_one = await service.get_length(filter_key="id", filter_value=1)
    assert exactly_one == 1


@pytest.mark.asyncio
async def test_product_find_page(service):
    res = await service.find_page(
        filter_key="status",
        filter_value=[1],
        sort_key="price",
        sort_direction="asc",
        page=1,
        page_size=10,
    )
    assert len(res) == 10


@pytest.mark.asyncio
async def test_product_search(service):
    res: List[ProductEntity] = await service.search(
        queries=[
            [OperatorEnum.IN, "category", [1, 2, 3]],
            [OperatorEnum.EQUAL, "status", 1],
        ],
        sort_key="best.price",
        direction="asc",
        page=2,
        page_size=5,
    )
    assert len(res) > 0
    assert sorted(res, key=lambda x: x.best.price) == res
    for p in res:
        assert p.status == 1
        assert p.category in [1, 2, 3]
