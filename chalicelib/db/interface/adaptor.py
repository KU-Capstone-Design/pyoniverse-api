from abc import ABCMeta


class DBAdaptor(metaclass=ABCMeta):
    def __init__(self, conn_uri: str):
        self._conn_uri = conn_uri
