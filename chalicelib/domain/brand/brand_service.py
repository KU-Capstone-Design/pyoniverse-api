from typing import Type

from chalice import BadRequestError
from overrides import override

from chalicelib.interface.factories.repository_factory import RepositoryFactory
from chalicelib.interface.repository import Repository
from chalicelib.interface.service import Service


class BrandService(Service):
    repository: Type[Repository] = RepositoryFactory.create_repository(
        "brand_mongo_repository"
    )

    @classmethod
    @override
    def get_single(cls, **kwargs) -> object:
        brand = cls.repository.find_by_slug(kwargs["slug"])
        if not brand:
            raise BadRequestError(f"Invalid slug: {kwargs['slug']}")
        return brand
