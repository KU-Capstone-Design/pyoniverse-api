from abc import ABCMeta, abstractmethod
from typing import Any, List, Literal, Sequence, Set

from chalicelib.entity.brand import BrandEntity
from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.entity.event import EventEntity
from chalicelib.entity.product import ProductEntity


class ServiceIfs(metaclass=ABCMeta):
    pass


class ProductServiceIfs(ServiceIfs):
    @abstractmethod
    def find_chunk(
        self, sort_key: str, direction: Literal["asc", "desc"], chunk_size: int
    ) -> Sequence[ProductEntity]:
        pass

    @abstractmethod
    def find_chunk_by(
        self,
        filter_key: str,
        filter_value: Any,
        sort_key: str,
        direction: Literal["asc", "desc"],
        chunk_size: int,
    ):
        pass

    @abstractmethod
    def find_one(self, entity: ProductEntity) -> ProductEntity:
        pass

    @abstractmethod
    def add_values(self, entity: ProductEntity) -> ProductEntity:
        pass

    @abstractmethod
    def find_in_sort_by(
        self,
        filter_key: str,
        filter_value: list,
        sort_key: str,
        direction: Literal["asc", "desc"],
    ):
        pass

    @abstractmethod
    def random(self, chunk_size: int):
        pass

    @abstractmethod
    def get_length(self, queries: List[list]) -> int:
        """
        :param queries: [OperatorEnum, attr, value] 순서의 리스트의 리스트
        """
        pass

    @abstractmethod
    def find_page(
        self,
        filter_key: str,
        filter_value: Any,
        sort_key: str,
        sort_direction: Literal["asc", "desc"],
        page: int,
        page_size: int,
    ):
        pass

    @abstractmethod
    def search(
        self,
        queries: List[list],
        sort_key: str,
        direction: Literal["asc", "desc"],
        page: int,
        page_size: int,
    ) -> List[ProductEntity]:
        """
        :param queries: [OperatorEnum, attr, value] 순서의 리스트의 리스트
        """
        pass

    @abstractmethod
    def distinct(self, attr: str, queries: List[list]) -> Set[Any]:
        """
        :param attr: 가져올 속성
        :param queries: [OperatorEnum, attr, value] 순서의 리스트의 리스트
        """
        pass


class EventServiceIfs(ServiceIfs):
    @abstractmethod
    def find_chunk(
        self, sort_key: str, direction: Literal["asc", "desc"], chunk_size: int
    ) -> Sequence[EventEntity]:
        pass

    @abstractmethod
    def find_chunk_by(
        self,
        filter_key: str,
        filter_value: Any,
        sort_key: str,
        direction: Literal["asc", "desc"],
        chunk_size: int,
    ):
        pass

    @abstractmethod
    def find_by_id(self, entity: EventEntity) -> EventEntity:
        pass

    @abstractmethod
    def find_all_by_brand(self, id: int) -> Sequence[EventEntity]:
        pass

    @abstractmethod
    def add_values(self, entity: ProductEntity) -> ProductEntity:
        pass


class BrandServiceIfs(ServiceIfs):
    @abstractmethod
    def find_by_slug(self, entity: BrandEntity) -> BrandEntity:
        pass


class ConstantBrandServiceIfs(ServiceIfs):
    @abstractmethod
    def find_all(self) -> Sequence[ConstantBrandEntity]:
        pass

    @abstractmethod
    def find_by_slug(self, entity: ConstantBrandEntity) -> ConstantBrandEntity:
        pass


class SearchServiceIfs(ServiceIfs):
    @abstractmethod
    def find_products(self, query: str) -> Sequence[int]:
        """
        :param query: 검색 쿼리
        :return: 검색 결과 ID List
        """
        pass
