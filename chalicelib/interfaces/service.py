from abc import ABCMeta
from typing import Tuple, Type

from chalicelib.models.pagination import Pagination
from chalicelib.interfaces.repository import Repository


class Service(metaclass=ABCMeta):
    repository: Type[Repository] = None

    @classmethod
    def get_single(cls, **kwargs) -> object:
        raise NotImplementedError

    @classmethod
    def get_list(cls, **kwargs) -> list:
        raise NotImplementedError

    @classmethod
    def get_paginated(cls, **kwargs) -> Tuple[list, Pagination]:
        raise NotImplementedError
