from abc import ABCMeta, abstractmethod
from typing import Any, Literal

from chalicelib.service.interface.command import (
    AddModifyEqualCommandIfs,
    EqualCommandIfs,
    SelectAllByCommandIfs,
    SelectAllCommandIfs,
    SelectBySortByCommandIfs,
    SelectInSortByCommandIfs,
    SortByLimit10CommandIfs,
)


class CommandFactoryIfs(metaclass=ABCMeta):
    @abstractmethod
    def get_equal_command(
        self, db_name: str, rel_name: str, key: str, value: Any
    ) -> EqualCommandIfs:
        pass

    @abstractmethod
    def get_sort_by_limit10_command(
        self, db_name: str, rel_name: str, key: str, value: Any
    ) -> SortByLimit10CommandIfs:
        pass

    @abstractmethod
    def get_select_all_command(
        self,
        db_name: str,
        rel_name: str,
        key: str,
        value: Any,
    ) -> SelectAllCommandIfs:
        pass

    @abstractmethod
    def get_select_all_by_command(
        self,
        db_name: str,
        rel_name: str,
        key: str,
        value: Any,
    ) -> SelectAllByCommandIfs:
        pass

    @abstractmethod
    def get_add_modify_equal_command(
        self, db_name: str, rel_name: str, key: str, value: Any, data: dict
    ) -> AddModifyEqualCommandIfs:
        pass

    @abstractmethod
    def get_select_by_sort_by_command(
        self,
        db_name: str,
        rel_name: str,
        key: str,
        value: Any,
        sort_key: str,
        sort_value: Literal["asc", "desc"],
        chunk_size: int = None,
    ) -> SelectBySortByCommandIfs:
        pass

    @abstractmethod
    def get_select_in_sort_by_command(
        self,
        db_name: str,
        rel_name: str,
        key: str,
        value: list,
        sort_key: str,
        sort_value: Literal["asc", "desc"],
    ) -> SelectInSortByCommandIfs:
        pass
