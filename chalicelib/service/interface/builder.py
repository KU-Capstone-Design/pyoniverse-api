from abc import ABCMeta, abstractmethod
from typing import Any, Literal

from chalicelib.business.model.enum import OperatorEnum
from chalicelib.service.model.result import Result


class BuilderIfs(metaclass=ABCMeta):
    @abstractmethod
    def project(self, attr: str) -> "BuilderIfs":
        pass

    @abstractmethod
    def where(self, op: OperatorEnum, attr: str, val: Any) -> "BuilderIfs":
        pass

    @abstractmethod
    def order(self, attr: str, direction: Literal["asc", "desc"]) -> "BuilderIfs":
        pass

    @abstractmethod
    def and_(self) -> "BuilderIfs":
        pass

    @abstractmethod
    def or_(self) -> "BuilderIfs":
        pass

    @abstractmethod
    def limit(self, n: int) -> "BuilderIfs":
        pass

    @abstractmethod
    def skip(self, n: int) -> "BuilderIfs":
        pass

    @abstractmethod
    def read(self) -> Result:
        pass

    @abstractmethod
    def update(self, **attrs) -> Result:
        pass

    @abstractmethod
    def random(self, n: int) -> Result:
        pass

    @abstractmethod
    def count(self) -> int:
        pass
