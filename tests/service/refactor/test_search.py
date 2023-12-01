import asyncio
import logging
import os
import time

import pytest

from chalicelib.service.search.service import AsyncSearchService


@pytest.fixture
def service(env):
    return AsyncSearchService(os.getenv("SEARCH_ENGINE_URI"))


@pytest.mark.asyncio
async def test_find_products(service):
    # given
    query = "우유"
    # when
    result = await service.find_products(query)
    # then
    assert len(result) > 0


@pytest.mark.asyncio
async def test_find_products_cache(service):
    # given
    query = "우유"
    # when
    s = time.time()
    result1 = await service.find_products(query)
    elapsed1 = time.time() - s
    s = time.time()
    result2 = await service.find_products(query)
    elapsed2 = time.time() - s
    # then
    assert len(result1) > 0
    assert result1 == result2
    assert elapsed2 < elapsed1
    logging.info(f"elapsed1: {elapsed1}, elapsed2: {elapsed2}")
