from typing import Type

from chalice import BadRequestError
from overrides import override

from chalicelib.factories.repository_factory import RepositoryFactory
from chalicelib.interfaces.repository import Repository
from chalicelib.interfaces.service import Service


class HomeService(Service):
    repository: Type[Repository] = RepositoryFactory.create_repository(
        "home_mongo_repository"
    )

    @classmethod
    @override
    def get_list(cls, **kwargs) -> list:
        match kwargs["type"]:
            case "stores":
                res = [
                    {
                        "id": 1,
                        "slug": "cu",
                        "brand": "CU",
                        "name": "CU",
                        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/"
                        "1a/CU_BI_%282017%29.svg/440px-CU_BI_%282017%29.svg.png",
                        "image-alt": "yyy",
                    },
                    {
                        "id": 2,
                        "slug": "gs25",
                        "brand": "GS25",
                        "name": "GS25",
                        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/GS25_bi_%282019%"
                        "29.svg/400px-GS25_bi_%282019%29.svg.png",
                        "image-alt": "yyy",
                    },
                ]
            case "events":
                res = [
                    {
                        "id": 1,
                        "brand": "gs25",
                        "slug": "gs25",
                        "name": "GS25",
                        "image": "https://hpsimg.gsretail.com/medias"
                        "/sys_master/images/images/h96/ha6/9088902135838.jpg",
                    },
                    {
                        "id": 1,
                        "brand": "gs25",
                        "slug": "gs25",
                        "name": "GS25",
                        "image": "https://hpsimg.gsretail.com/medias"
                        "/sys_master/images/images/h96/ha6/9088902135838.jpg",
                    },
                ]
            case "products":
                res = [
                    {
                        "id": 1,
                        "name": "11가지찬많은도시락1편",
                        "events": None,
                        "image": "s3://pyoniverse-image/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                        "image-alt": "yyy",
                    },
                    {
                        "id": 1,
                        "name": "11가지찬많은도시락1편",
                        "events": None,
                        "image": "s3://pyoniverse-image/products/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
                        "image-alt": "yyy",
                    },
                ]
            case _:
                raise BadRequestError(
                    f"Invalid type: {type}. Valid types are: stores, events, products"
                )
        return res
