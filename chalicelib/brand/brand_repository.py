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
            "products": {
                "events": ["1+1", "2+1"],
                "1+1": {
                    "total": [
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                    ],
                    "food": [
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                    ],
                },
                "2+1": {
                    "snack": [
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                    ],
                    "food": [
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                        {
                            "id": 0,
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com"
                            "/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                            "image_alt": "food",
                            "name": "11가지찬많은도시락1편",
                        },
                    ],
                },
            },
        }
