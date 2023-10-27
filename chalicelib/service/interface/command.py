from abc import ABCMeta, abstractmethod
from typing import Any, Literal, Sequence

from chalicelib.entity.base import EntityType


class CommandIfs(metaclass=ABCMeta):
    def __init__(
        self,
        rel_name: str,
        key: str,
        value: Any,
        db_name: Literal["constant", "service"] = "service",
    ):
        self._rel_name = rel_name
        self._key = key
        self._value = value
        self._db_name = db_name

    @abstractmethod
    def execute(self) -> Sequence[EntityType] | EntityType | None:
        pass


class EqualCommandIfs(CommandIfs):
    pass
