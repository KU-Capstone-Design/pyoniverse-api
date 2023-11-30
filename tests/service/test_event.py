from typing import Sequence

import pytest

from chalicelib.entity.event import EventEntity
from chalicelib.service.event.service import AsyncEventService


@pytest.mark.asyncio
async def test_event_service(factory, invoker):
    # given
    service = AsyncEventService(command_factory=factory, invoker=invoker)
    chunk_size = 2
    # when & then
    result = await service.find_chunk(
        sort_key="good_count", direction="desc", chunk_size=chunk_size
    )
    assert isinstance(result, list)
    assert 0 < len(result) <= 2
    assert all(isinstance(r, EventEntity) for r in result)
    assert sorted(result, key=lambda x: x.good_count, reverse=True) == result


@pytest.mark.asyncio
async def test_event_service_add_values(factory, invoker):
    # given
    service = AsyncEventService(command_factory=factory, invoker=invoker)
    entity = EventEntity(id=1, good_count=1, view_count=2)
    # when
    prv_entity: EventEntity = await service.find_by_id(entity)
    result: EventEntity = await service.add_values(entity)
    # then
    assert isinstance(result, EventEntity)
    assert result.id == entity.id
    assert result.good_count == prv_entity.good_count + entity.good_count
    assert result.view_count == prv_entity.view_count + entity.view_count


@pytest.mark.asyncio
async def test_event_find_chunk_by(factory, invoker):
    # given
    service = AsyncEventService(command_factory=factory, invoker=invoker)
    # when
    coroutine = service.find_chunk_by(
        filter_key="brand",
        filter_value=1,
        sort_key="good_count",
        direction="asc",
        chunk_size=3,
    )
    result: Sequence[EventEntity] = await coroutine
    assert isinstance(result, list)
