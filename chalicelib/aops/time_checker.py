import logging
import os
import time
from functools import wraps


logger = logging.getLogger("AOP Logger")
logger.setLevel(os.getenv("LOG_LEVEL", "DEBUG"))


def time_checker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        s = time.time_ns() // 1_000_000
        result = func(*args, **kwargs)
        e = time.time_ns() // 1_000_000
        logger.debug(f"Function {func.__name__} took {e - s} millisecond to execute")
        return result

    return wrapper
