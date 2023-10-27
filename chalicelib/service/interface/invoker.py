from abc import ABCMeta, abstractmethod
from typing import List, Sequence

from chalicelib.entity.base import EntityType
from chalicelib.service.interface.command import CommandIfs


class InvokerIfs(metaclass=ABCMeta):
    def __init__(self):
        self._commands: List[CommandIfs] = []

    def add_command(self, command: CommandIfs):
        self._commands.append(command)

    def pop_command(self) -> CommandIfs:
        return self._commands.pop()

    @abstractmethod
    def invoke(
        self,
    ) -> (
        Sequence[EntityType]
        | EntityType
        | None
        | Sequence[Sequence[EntityType] | EntityType | None]
    ):
        pass
