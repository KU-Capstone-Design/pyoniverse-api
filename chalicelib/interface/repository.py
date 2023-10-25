from abc import ABCMeta
from typing import Optional, Tuple, TypeVar

from chalicelib.common.model.pagination import Pagination
from chalicelib.interface.adaptor import AdaptorType


class Repository(metaclass=ABCMeta):
    def __init__(self, adaptor: AdaptorType):
        self._adaptor = adaptor

    def find_by_id(self, id, **kwargs) -> Optional[object]:
        raise NotImplementedError

    def find_by_slug(self, slug, **kwargs) -> Optional[object]:
        raise NotImplementedError

    def find(self, **kwargs) -> list:
        raise NotImplementedError

    def paginate(self, **kwargs) -> Tuple[list, Pagination]:
        raise NotImplementedError


RepositoryType = TypeVar("RepositoryType", bound=Repository)
