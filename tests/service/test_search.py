import asyncio
import logging
import os
import time

import dotenv
import pytest

from chalicelib.service.search.service import AsyncSearchService


while "tests" not in os.listdir():
    os.chdir("..")

dotenv.load_dotenv()


@pytest.fixture
def service():
    return AsyncSearchService(os.getenv("SEARCH_ENGINE_URI"))


def test_find_products(service):
    loop = asyncio.get_event_loop()
    # given
    query = "우유"
    # when
    result = loop.run_until_complete(service.find_products(query))
    # then
    assert len(result) > 0


def test_find_products_cache(service):
    # given
    query = "우유"
    loop = asyncio.get_event_loop()
    # when
    s = time.time()
    result1 = loop.run_until_complete(service.find_products(query))
    elapsed1 = time.time() - s
    s = time.time()
    result2 = loop.run_until_complete(service.find_products(query))
    elapsed2 = time.time() - s
    # then
    assert len(result1) > 0
    assert result1 == result2
    assert elapsed2 < elapsed1
    logging.info(f"elapsed1: {elapsed1}, elapsed2: {elapsed2}")
