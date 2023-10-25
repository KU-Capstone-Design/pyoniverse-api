import logging
from asyncio import AbstractEventLoop

from motor import motor_asyncio
from pymongo.errors import ConnectionFailure

from chalicelib.interface.adaptor import DBAdaptor


class MongoAdaptor(DBAdaptor):
    def __init__(self, conn_uri: str):
        super().__init__(conn_uri)
        self.client = motor_asyncio.AsyncIOMotorClient(self._conn_uri)
        loop: AbstractEventLoop = self.client.get_io_loop()
        loop.run_until_complete(self.__ping())

    async def __ping(self):
        try:
            self.client.admin.command("ping")
            logging.info("Connect to mongo server")
        except ConnectionFailure as e:
            logging.error("Server not available")
            raise e
