from typing import Type

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
        return [
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
