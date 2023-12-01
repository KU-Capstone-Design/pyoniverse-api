from abc import ABCMeta, abstractmethod

from chalicelib.service_refactor.interface.builder import BuilderIfs


class FactoryIfs(metaclass=ABCMeta):
    @abstractmethod
    def make(self) -> BuilderIfs:
        pass
