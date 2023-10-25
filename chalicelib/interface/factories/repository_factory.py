from typing import Type

from chalicelib.db.brand.repository import BrandMongoRepository
from chalicelib.db.event.repository import EventMongoRepository
from chalicelib.db.home.repository import HomeMongoRepository
from chalicelib.db.product.repository import ProductMongoRepository
from chalicelib.interface.repository import Repository


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
