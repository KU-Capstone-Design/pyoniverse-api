from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.persistant.refactor.builder import AsyncMongoBuilder
from chalicelib.service_refactor.interface.factory import FactoryIfs


class AsyncMongoFactory(FactoryIfs):
    def __init__(self, client: AsyncIOMotorClient):
        self.__client = client

    def make(self, db: str, rel: str) -> AsyncMongoBuilder:
        return AsyncMongoBuilder(
            db_name=db,
            rel_name=rel,
            rel=self.__client.get_database(db).get_collection(rel),
        )
