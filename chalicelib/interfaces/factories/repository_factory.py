from typing import Type

from chalicelib.domain.brand.brand_repository import BrandMongoRepository
from chalicelib.domain.event.event_repository import EventMongoRepository
from chalicelib.domain.home.home_repository import HomeMongoRepository
from chalicelib.interfaces.repository import Repository
from chalicelib.domain.product.product_repository import ProductMongoRepository


class RepositoryFactory:
    @staticmethod
    def create_repository(name: str) -> Type[Repository]:
        match name:
            case "product_mongo_repository":
                return ProductMongoRepository
            case "event_mongo_repository":
                return EventMongoRepository
            case "home_mongo_repository":
                return HomeMongoRepository
            case "brand_mongo_repository":
                return BrandMongoRepository
            case _:
                raise RuntimeError(f"Repository {name} not found")
