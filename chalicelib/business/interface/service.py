from abc import ABCMeta, abstractmethod

from chalicelib.entity.brand import BrandEntity


class ServiceIfs(metaclass=ABCMeta):
    pass


class ProductServiceIfs(ServiceIfs):
    pass


class EventServiceIfs(ServiceIfs):
    pass


class BrandServiceIfs(ServiceIfs):
    @abstractmethod
    def find_by_slug(self, entity: BrandEntity) -> BrandEntity:
        pass
