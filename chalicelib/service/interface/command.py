import logging
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


class SortByLimit10CommandIfs(CommandIfs):
    """
    key: sort_key
    value: 1(ascending) or -1(descending)
    """

    pass


class SelectAllCommandIfs(CommandIfs):
    """
    key: sort_key
    value: 1(ascending) or -1(descending)
    """

    pass


class SelectAllByCommandIfs(CommandIfs):
    """
    key: filter_key
    value: Any
    """

    pass


class ModifyCommandIfs(CommandIfs):
    def __init__(
        self,
        rel_name: str,
        key: str,
        value: Any,
        data: dict,
        db_name: Literal["constant", "service"] = "service",
    ):
        """
        :param rel_name: Relation Name
        :param key: Filter Key
        :param value: Filter Value
        :param data: 갱신될 데이터
        :param db_name: Db Name
        """
        super().__init__(
            rel_name=rel_name,
            key=key,
            value=value,
            db_name=db_name,
        )
        self._data = data


class AddModifyEqualCommandIfs(ModifyCommandIfs):
    """
    key: filter_key
    value: filter_value
    cond: equal condition

    data: 갱신할 값(기존값 + 갱신 데이터로 변경됨)
    """

    pass
