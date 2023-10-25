from pymongo import MongoClient

from chalicelib.db.interface.adaptor import DBAdaptor


class MongoAdaptor(DBAdaptor):
    def __init__(self, conn_uri: str):
        super().__init__(conn_uri)
        self.client = MongoClient(self._conn_uri)
