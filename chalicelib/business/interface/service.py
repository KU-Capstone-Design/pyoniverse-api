from abc import ABCMeta


class ServiceIfs(metaclass=ABCMeta):
    pass


class ProductServiceIfs(ServiceIfs):
    pass


class EventServiceIfs(ServiceIfs):
    pass


class BrandServiceIfs(ServiceIfs):
    pass
