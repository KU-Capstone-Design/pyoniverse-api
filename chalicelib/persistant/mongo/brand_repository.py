import os
from typing import Optional

from overrides import override
from pymongo import ReadPreference

from chalicelib.extern.aop.time_checker import time_checker
from chalicelib.persistant.mongo.adaptor import MongoAdaptor
from chalicelib.interface.repository import Repository


class BrandMongoRepository(Repository):
    def __init__(self, adaptor: MongoAdaptor):
        super().__init__(adaptor=adaptor)
        self.__client = adaptor.client
        self.__db = self.__client.get_database(
            os.getenv("MONGO_DB"), read_preference=ReadPreference.SECONDARY_PREFERRED
        )

    @time_checker
    @override
    def find_by_slug(self, slug, **kwargs) -> Optional[object]:
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
                    # TODO : DB 연동
                    "start_at": "2023-10-01",
                    "end_at": "2023-10-31",
                }
            ],
            "products": [
                {
                    "id": 0,
                    "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                    "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                    "image_alt": "food",
                    "name": "11가지찬많은도시락1편",
                    "price": 1000.0,
                    "good_count": 300,
                },
                {
                    "id": 0,
                    "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                    "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                    "image_alt": "food",
                    "name": "11가지찬많은도시락1편",
                    "price": 1000.0,
                    "good_count": 200,
                },
                {
                    "id": 0,
                    "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                    "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                    "image_alt": "food",
                    "name": "11가지찬많은도시락1편",
                    "price": 1000.0,
                    "good_count": 100,
                },
            ],
        }
