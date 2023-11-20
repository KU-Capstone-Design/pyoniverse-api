import asyncio

import pytest

from chalicelib.extern.util import async_cache


@async_cache
async def f(x: int) -> int:
    return x


def test_awaitable_lru_cache_error_case():
    loop = asyncio.get_event_loop()
    x = loop.run_until_complete(f(1))
    loop.run_until_complete(f(1))
    y = loop.run_until_complete(f(2))

    assert y == 2 and x == 1

    with pytest.raises(RuntimeError):

        @async_cache
        def not_coroutine(x: int) -> x:
            return x
