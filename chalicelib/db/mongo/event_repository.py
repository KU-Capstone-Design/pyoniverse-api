import os

from pymongo import ReadPreference

from chalicelib.db.mongo.adaptor import MongoAdaptor
from chalicelib.interface.repository import Repository


class EventMongoRepository(Repository):
    def __init__(self, adaptor: MongoAdaptor):
        super().__init__(adaptor=adaptor)
        self.__client = adaptor.client
        self.__db = self.__client.get_database(
            os.getenv("MONGO_DB"), read_preference=ReadPreference.SECONDARY_PREFERRED
        )
