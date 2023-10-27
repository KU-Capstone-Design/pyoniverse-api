from abc import ABCMeta, abstractmethod
from typing import Any

from chalicelib.service.interface.command import EqualCommandIfs


class CommandFactoryIfs(metaclass=ABCMeta):
    @abstractmethod
    def get_equal_command(
        self, db_name: str, rel_name: str, key: str, value: Any
    ) -> EqualCommandIfs:
        pass
