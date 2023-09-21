from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple

from chalicelib.dtos.pagination import Pagination


class Repository(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def find_by_id(cls, id, **kwargs) -> Optional[object]:
        pass

    @classmethod
    def find_by_slug(cls, slug, **kwargs) -> Optional[object]:
        raise NotImplementedError

    @classmethod
    def find(cls, **kwargs) -> list:
        raise NotImplementedError

    @classmethod
    def paginate(cls, **kwargs) -> Tuple[list, Pagination]:
        raise NotImplementedError
