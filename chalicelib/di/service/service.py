from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Dependency, Singleton

from chalicelib.domain.brand.brand_service import BrandService
from chalicelib.domain.event.event_service import EventService
from chalicelib.domain.home.home_service import HomeService
from chalicelib.domain.product.product_service import ProductService
from chalicelib.interface.repository import Repository
from chalicelib.interface.service import Service


class ServiceProvider(Singleton):
    provided_type = Service


class ServiceContainer(DeclarativeContainer):
    home_repository = Dependency(Repository)
    brand_repository = Dependency(Repository)
    event_repository = Dependency(Repository)
    product_repository = Dependency(Repository)
    # constant_repository = Dependency(Repository)

    wiring_config = WiringConfiguration(packages=["chalicelib.service"])


class ServiceInjector(ServiceContainer):
    home_service = ServiceProvider(
        HomeService, repository=ServiceContainer.home_repository
    )
    brand_service = ServiceProvider(
        BrandService, repository=ServiceContainer.brand_repository
    )
    product_service = ServiceProvider(
        ProductService, repository=ServiceContainer.product_repository
    )
    event_service = ServiceProvider(
        EventService, repository=ServiceContainer.event_repository
    )
