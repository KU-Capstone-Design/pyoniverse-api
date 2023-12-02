from abc import ABCMeta, abstractmethod

from chalicelib.service.interface.builder import BuilderIfs


class FactoryIfs(metaclass=ABCMeta):
    @abstractmethod
    def make(self, db: str, rel: str) -> BuilderIfs:
        pass
