from typing import Type

from chalice import BadRequestError
from overrides import override

from chalicelib.dtos.converter import IdConverter
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
                res = cls.repository.find(type="brand")
                for brand in res:
                    brand["brand"] = brand["name"].upper()
                    brand["image-alt"] = f"{brand['brand']} Logo"

            case "events":
                res = cls.repository.find(type="event")
                for event in res:
                    event["brand"] = IdConverter.convert_brand_id(event["brand"])[
                        "name"
                    ].upper()
                    event["image"] = event["image"]["thumb"]
                    event["image-alt"] = f"({event['brand']}) {event['name']}"
                return res
            case "products":
                res = cls.repository.find(type="product")
                for product in res:
                    product["events"] = None
                    product["image-alt"] = f"{product['name']} thumbnail"
                return res
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
