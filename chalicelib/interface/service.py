from abc import ABCMeta
from typing import Tuple

from chalicelib.common.model.pagination import Pagination
from chalicelib.interface.repository import Repository


class Service(metaclass=ABCMeta):
    def __init__(self, repository: Repository):
        self._repository = repository

    def get_single(self, **kwargs) -> object:
        raise NotImplementedError

    def get_list(self, **kwargs) -> list:
        raise NotImplementedError

    def get_paginated(self, **kwargs) -> Tuple[list, Pagination]:
        raise NotImplementedError
