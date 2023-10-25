import logging

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from chalicelib.interface.adaptor import DBAdaptor


class MongoAdaptor(DBAdaptor):
    def __init__(self, conn_uri: str):
        super().__init__(conn_uri)
        try:
            # The ping command is cheap and does not require auth.
            self.client = MongoClient(self._conn_uri)
            self.client.admin.command("ping")
            logging.info("Connect to mongo server")
        except ConnectionFailure:
            logging.error("Server not available")
