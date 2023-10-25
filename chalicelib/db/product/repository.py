import os

from dependency_injector.wiring import Provide, inject
from pymongo import ReadPreference

from chalicelib.db.adaptor.mongo import MongoAdaptor
from chalicelib.interface.repository import Repository


class ProductMongoRepository(Repository):
    @inject
    def __init__(self, adaptor: MongoAdaptor):
        self.__client = adaptor.client
        self.__db = self.__client.get_database(
            os.getenv("MONGO_DB"), read_preference=ReadPreference.SECONDARY_PREFERRED
        )
