import pytest

from chalicelib.entity.product import ProductEntity
from chalicelib.service.product.service import AsyncProductService


@pytest.fixture
def product_service(factory, invoker):
    return AsyncProductService(command_factory=factory, invoker=invoker)


@pytest.mark.asyncio
async def test_product_service_find_chunk(factory, invoker):
    # given
    service = AsyncProductService(command_factory=factory, invoker=invoker)
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
async def test_product_service_find_one(factory, invoker):
    # given
    service = AsyncProductService(command_factory=factory, invoker=invoker)
    entity = ProductEntity(id=1)
    # when & then
    result = await service.find_one(entity)
    assert isinstance(result, ProductEntity)
    assert result.id == entity.id


@pytest.mark.asyncio
async def test_product_service_add_values(factory, invoker):
    # given
    service = AsyncProductService(command_factory=factory, invoker=invoker)
    entity = ProductEntity(id=1, good_count=1, view_count=2)
    # when
    prv_entity: ProductEntity = await service.find_one(entity)
    result: ProductEntity = await service.add_values(entity)
    # then
    assert isinstance(result, ProductEntity)
    assert result.id == entity.id
    assert result.good_count == prv_entity.good_count + entity.good_count
    assert result.view_count == prv_entity.view_count + entity.view_count


@pytest.mark.asyncio
async def test_product_length(factory, invoker):
    service = AsyncProductService(command_factory=factory, invoker=invoker)
    res = await service.get_length()
    assert res > 0
    exactly_one = await service.get_length(filter_key="id", filter_value=1)
    assert exactly_one == 1


@pytest.mark.asyncio
async def test_product_find_page(product_service):
    res = await product_service.find_page(
        filter_key="status",
        filter_value=1,
        sort_key="price",
        sort_direction="asc",
        page=1,
        page_size=10,
    )
    assert len(res) == 10
