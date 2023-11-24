import asyncio
from functools import lru_cache, wraps


def async_cache(f=None):
    """
    :param f: Coroutine Function
    :return:
    """
    # Check f is coroutine
    if not asyncio.iscoroutinefunction(f):
        raise RuntimeError(f"{f} is not coroutine")

    loop = asyncio.get_event_loop()

    @lru_cache
    def __cached_func(*args, **kwargs):
        res = loop.run_until_complete(f(*args, **kwargs))
        return res

    @wraps(f)
    def wrapper(*args, **kwargs):
        res = __cached_func(*args, **kwargs)
        future = loop.create_future()
        future.set_result(res)
        return future

    return wrapper
