from abc import ABCMeta
from typing import TypeVar


class DBAdaptor(metaclass=ABCMeta):
    def __init__(self, conn_uri: str):
        self._conn_uri = conn_uri


AdaptorType = TypeVar("AdaptorType", bound=DBAdaptor)
