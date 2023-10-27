from abc import ABCMeta, abstractmethod
from typing import Any

from chalicelib.service.interface.command import (
    EqualCommandIfs,
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
