from abc import ABCMeta
from typing import Optional, Tuple

from chalicelib.models.pagination import Pagination


class Repository(metaclass=ABCMeta):
    @classmethod
    def find_by_id(cls, id, **kwargs) -> Optional[object]:
        raise NotImplementedError

    @classmethod
    def find_by_slug(cls, slug, **kwargs) -> Optional[object]:
        raise NotImplementedError

    @classmethod
    def find(cls, **kwargs) -> list:
        raise NotImplementedError

    @classmethod
    def paginate(cls, **kwargs) -> Tuple[list, Pagination]:
        raise NotImplementedError
