import os
from asyncio import AbstractEventLoop

from motor.motor_asyncio import AsyncIOMotorDatabase
from overrides import override
from pymongo import DESCENDING, ReadPreference

from chalicelib.aop.time_checker import time_checker
from chalicelib.db.mongo.adaptor import MongoAdaptor
from chalicelib.interface.repository import Repository


class HomeMongoRepository(Repository):
    def __init__(self, adaptor: MongoAdaptor):
        super().__init__(adaptor=adaptor)
        self.__client = adaptor.client
        self.__loop: AbstractEventLoop = self.__client.get_io_loop()
        self.__db: AsyncIOMotorDatabase = self.__client.get_database(
            os.getenv("MONGO_DB"), read_preference=ReadPreference.SECONDARY_PREFERRED
        )
        self.__constant_db: AsyncIOMotorDatabase = self.__client.get_database(
            "constant", read_preference=ReadPreference.SECONDARY_PREFERRED
        )

    @time_checker
    @override
    def find(self, **kwargs) -> list:
        match kwargs["type"]:
            case "brand":
                cursor = self.__constant_db["brands"].find(
                    projection={
                        "_id": False,
                        "name": True,
                        "slug": True,
                        "image": True,
                    },
                    hint=[("slug", 1)],
                )
                return self.__loop.run_until_complete(cursor.to_list(length=None))
            case "event":
                cursor = (
                    self.__db["events"]
                    .find(
                        projection={
                            "_id": False,
                            "id": True,
                            "name": True,
                            "brand": True,
                            "image": True,
                        },
                    )
                    .hint([("id", 1)])
                    .sort("id", 1)
                    .limit(5)
                )
                return self.__loop.run_until_complete(cursor.to_list(length=None))
            case "product":
                cursor = (
                    self.__db["products"]
                    .find(
                        projection={
                            "_id": False,
                            "id": True,
                            "name": True,
                            "image": True,
                            "price": True,
                            "best": True,
                            "good_count": True,
                        },
                    )
                    .hint([("good_count", 1)])
                    .sort("good_count", DESCENDING)
                    .limit(6)
                )
                return self.__loop.run_until_complete(cursor.to_list(length=None))
            case _:
                raise NotImplementedError("This type is not implemented")
