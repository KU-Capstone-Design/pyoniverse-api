from abc import ABCMeta
from typing import TypeVar

from chalice import Blueprint

from chalicelib.interface.service import ServiceType


class Controller(metaclass=ABCMeta):
    api: Blueprint
    service: ServiceType


ControllerType = TypeVar("ControllerType", bound=Controller)
