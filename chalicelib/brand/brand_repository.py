import os
from typing import Optional

from overrides import override
from pymongo import MongoClient, ReadPreference

from chalicelib.aops.time_checker import time_checker
from chalicelib.interfaces.repository import Repository


class BrandMongoRepository(Repository):
    __client = MongoClient(os.getenv("MONGO_URI"))
    __db = __client.get_database(
        os.getenv("MONGO_DB"), read_preference=ReadPreference.SECONDARY_PREFERRED
    )

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("This class should not be instantiated")

    @classmethod
    @time_checker
    @override
    def find_by_slug(cls, slug, **kwargs) -> Optional[object]:
        return {
            "slug": "cu",
            "id": 0,
            "name": "CU Store",
            "meta": {"description": "CU Store Main Page"},
            "description": "Description",
            "events": [
                {
                    "brand": "CU",
                    "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                    "/events/18ae49979b0050484fb8a0a86415ac3f248284fb.webp",
                    "name": "cu 와인 라벨 패키지 공모전",
                    "id": 1,
                    "image_alt": "(CU) cu 와인 라벨 패키지 공모전",
                }
            ],
            "products": [
                {
                    "event": "1+1",
                    "category": "total",
                    "items": [
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/events/18ae49979b0050484fb8a0a86415ac3f248284fb.webp",
                            "image_alt": "food",
                            "name": "Food",
                        }
                    ],
                },
                {
                    "event": "1+1",
                    "category": "total",
                    "items": [
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/events/18ae49979b0050484fb8a0a86415ac3f248284fb.webp",
                            "image_alt": "food",
                            "name": "Food",
                        }
                    ],
                },
            ],
        }
