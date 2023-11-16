import asyncio
import os

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
    # given
    query = "우유"
    loop = asyncio.get_event_loop()
    # when
    result = loop.run_until_complete(service.find_products(query))
    # then
    assert len(result) > 0


# def test_find_products_invalid(service):
#     # given
#     query = "이것은 아무런 값도 반환하면 안됩니다."
#     loop = asyncio.get_event_loop()
#     # when
#     result = loop.run_until_complete(service.find_products(query))
#     # then
#     assert len(result) == 0
