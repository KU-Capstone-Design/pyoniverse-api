from abc import ABCMeta, abstractmethod
from asyncio import Future
from typing import Any, Sequence

from chalicelib.entity.base import EntityType


class CommandIfs(metaclass=ABCMeta):
    def __init__(self, key: str, value: Any):
        self._key = key
        self._value = value

    @abstractmethod
    def execute(self) -> Sequence[EntityType] | EntityType | None | Future:
        pass
