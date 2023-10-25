from abc import ABCMeta
from typing import TypeVar

from chalicelib.interface.repository import RepositoryType


class Service(metaclass=ABCMeta):
    def __init__(self, repository: RepositoryType):
        self._repository = repository


ServiceType = TypeVar("ServiceType", bound=Service)
