from abc import ABCMeta, abstractmethod

from chalicelib.business.interface.dto import DtoType


class BusinessIfs(metaclass=ABCMeta):
    pass


class ProductBusinessIfs(BusinessIfs):
    pass


class EventBusinessIfs(BusinessIfs):
    pass


class BrandBusinessIfs(BusinessIfs):
    @abstractmethod
    def get_detail_page(self, request: DtoType) -> DtoType:
        pass


class HomeBusinessIfs(BusinessIfs):
    @abstractmethod
    def get_list(self, request: DtoType) -> DtoType:
        pass
