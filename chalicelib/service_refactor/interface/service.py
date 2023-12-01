from chalicelib.business.interface.service import ServiceIfs
from chalicelib.service_refactor.interface.factory import FactoryIfs


class AbstractService(ServiceIfs):
    def __init__(self, factory: FactoryIfs):
        self._factory = factory
