from abc import ABCMeta, abstractmethod

from chalicelib.business.interface.dto import DtoType


class BusinessIfs(metaclass=ABCMeta):
    pass


class ProductBusinessIfs(BusinessIfs):
    @abstractmethod
    def get_detail(self, request: DtoType) -> DtoType:
        pass


class EventBusinessIfs(BusinessIfs):
    def get_list(self, request: DtoType) -> DtoType:
        pass

    def get_detail(self, request: DtoType) -> DtoType:
        pass


class BrandBusinessIfs(BusinessIfs):
    @abstractmethod
    def get_detail_page(self, request: DtoType) -> DtoType:
        pass


class HomeBusinessIfs(BusinessIfs):
    @abstractmethod
    def get_list(self, request: DtoType) -> DtoType:
        pass


class SearchBusinessIfs(BusinessIfs):
    @abstractmethod
    def get_index(self) -> DtoType:
        pass

    @abstractmethod
    def get_result(self, request: DtoType) -> DtoType:
        pass


class MetricBusinessIfs(BusinessIfs):
    @abstractmethod
    def get_good_count(self, request: DtoType) -> DtoType:
        pass

    @abstractmethod
    def get_view_count(self, request: DtoType) -> DtoType:
        pass

    @abstractmethod
    def update_good_count(self, request: DtoType) -> DtoType:
        pass

    @abstractmethod
    def update_view_count(self, request: DtoType) -> DtoType:
        pass
