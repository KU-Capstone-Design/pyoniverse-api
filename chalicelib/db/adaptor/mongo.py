from pymongo import MongoClient

from chalicelib.interface.adaptor import DBAdaptor


class MongoAdaptor(DBAdaptor):
    def __init__(self, conn_uri: str):
        super().__init__(conn_uri)
        self.client = MongoClient(self._conn_uri)
