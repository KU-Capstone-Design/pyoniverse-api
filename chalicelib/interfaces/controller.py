from abc import ABCMeta
from typing import Type

from chalicelib.interfaces.service import Service


class Controller(metaclass=ABCMeta):
    service: Type[Service] = None
