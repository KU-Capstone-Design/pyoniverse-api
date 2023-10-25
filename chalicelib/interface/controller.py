from abc import ABCMeta
from typing import Type

from chalice import Blueprint

from chalicelib.interface.service import Service


class Controller(metaclass=ABCMeta):
    api: Blueprint = None
    service: Type[Service] = None
