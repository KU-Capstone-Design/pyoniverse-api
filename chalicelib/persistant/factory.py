import os

from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.persistant.builder import AsyncMongoBuilder
from chalicelib.service.interface.factory import FactoryIfs


class AsyncMongoFactory(FactoryIfs):
    def __init__(self, client: AsyncIOMotorClient):
        self.__client = client

    def make(self, db: str, rel: str) -> AsyncMongoBuilder:
        if db == "service":
            db_name = os.getenv("MONGO_DB")
        else:
            db_name = db
        return AsyncMongoBuilder(
            db_name=db,
            rel_name=rel,
            rel=self.__client.get_database(db_name).get_collection(rel),
        )
