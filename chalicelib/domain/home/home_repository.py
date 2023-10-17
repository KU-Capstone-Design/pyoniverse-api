import os

from overrides import override
from pymongo import DESCENDING, MongoClient, ReadPreference

from chalicelib.aop.time_checker import time_checker
from chalicelib.interfaces.repository import Repository


class HomeMongoRepository(Repository):
    __client = MongoClient(os.getenv("MONGO_URI"))
    __db = __client.get_database(
        os.getenv("MONGO_DB"), read_preference=ReadPreference.SECONDARY_PREFERRED
    )
    __constant_db = __client.get_database(
        "constant", read_preference=ReadPreference.SECONDARY_PREFERRED
    )

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("This class should not be instantiated")

    @classmethod
    @time_checker
    @override
    def find(cls, **kwargs) -> list:
        match kwargs["type"]:
            case "brand":
                res = cls.__constant_db["brands"].find(
                    projection={
                        "_id": False,
                        "name": True,
                        "slug": True,
                        "image": True,
                    },
                    hint=[("slug", 1)],
                )
                return list(res)
            case "event":
                res = (
                    cls.__db["events"]
                    .find(
                        projection={
                            "_id": False,
                            "id": True,
                            "name": True,
                            "brand": True,
                            "image": True,
                        },
                        hint=[("id", 1)],
                    )
                    .limit(5)
                )
                return list(res)
            case "product":
                res = (
                    cls.__db["products"]
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
                        hint=[("good_count", 1)],
                    )
                    .sort("good_count", DESCENDING)
                    .limit(6)
                )
                return list(res)
            case _:
                raise NotImplementedError("This type is not implemented")
