import logging
from functools import wraps


class SimpleAsyncCache:
    def __init__(self, func):
        self.__func = func
        self.__cache = {}
        self.logger = logging.getLogger(__name__)

    def get_key(self, *args, **kwargs):
        return f"{args}{kwargs}"

    async def __call__(self, *args, **kwargs):
        self.logger.debug(self.__cache)
        key = self.get_key(args, kwargs)
        if key not in self.__cache:
            val = await self.__func(*args, **kwargs)
            self.__cache[key] = val
        return self.__cache.get(key)


def async_cache(func):
    cache = SimpleAsyncCache(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        res = cache(*args, **kwargs)
        return res

    return wrapper
