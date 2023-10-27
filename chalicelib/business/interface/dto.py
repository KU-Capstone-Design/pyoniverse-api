from abc import ABCMeta
from typing import TypeVar


class DtoIfs(metaclass=ABCMeta):
    pass


DtoType = TypeVar("DtoType", bound=DtoIfs)
