from abc import ABCMeta, abstractmethod
from typing import Literal, Sequence

from chalicelib.entity.brand import BrandEntity
from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.entity.event import EventEntity


class ServiceIfs(metaclass=ABCMeta):
    pass


class ProductServiceIfs(ServiceIfs):
    @abstractmethod
    def find_chunk(
        self, sort_key: str, direction: Literal["asc", "desc"], chunk_size: int
    ) -> Sequence[EventEntity]:
        pass


class EventServiceIfs(ServiceIfs):
    @abstractmethod
    def find_chunk(
        self, sort_key: str, direction: Literal["asc", "desc"], chunk_size: int
    ) -> Sequence[EventEntity]:
        pass


class BrandServiceIfs(ServiceIfs):
    @abstractmethod
    def find_by_slug(self, entity: BrandEntity) -> BrandEntity:
        pass


class ConstantBrandServiceIfs(ServiceIfs):
    @abstractmethod
    def find_all(self) -> Sequence[ConstantBrandEntity]:
        pass
