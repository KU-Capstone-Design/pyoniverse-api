from abc import ABCMeta
from typing import Tuple, Type

from chalicelib.common.model.pagination import Pagination
from chalicelib.interface.repository import Repository


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
