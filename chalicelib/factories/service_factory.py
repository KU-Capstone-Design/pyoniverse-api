from typing import Type

from chalicelib.brand.brand_service import BrandService
from chalicelib.event.event_service import EventService
from chalicelib.home.home_service import HomeService
from chalicelib.interfaces.service import Service
from chalicelib.product.product_service import ProductService


class ServiceFactory:
    @staticmethod
    def create_service(name: str) -> Type[Service]:
        match name:
            case "product_service":
                return ProductService
            case "event_service":
                return EventService
            case "home_service":
                return HomeService
            case "brand_service":
                return BrandService
            case _:
                raise RuntimeError(f"Service {name} not found")
