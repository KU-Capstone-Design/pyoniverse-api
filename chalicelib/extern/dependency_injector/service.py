from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from chalicelib.business.interface.service import ServiceIfs
from chalicelib.service_refactor.constant_brand.service import AsyncConstantBrandService
from chalicelib.service_refactor.event.service import AsyncEventService
from chalicelib.service_refactor.interface.factory import FactoryIfs
from chalicelib.service_refactor.product.service import AsyncProductService
from chalicelib.service_refactor.search.service import AsyncSearchService


class ServiceProvider(Singleton):
    provided_type = ServiceIfs


class ServiceContainer(DeclarativeContainer):
    factory = Dependency(FactoryIfs)
    engine_uri = Dependency(str)


class ServiceInjector(ServiceContainer):
    constant_brand_service = ServiceProvider(
        AsyncConstantBrandService,
        factory=ServiceContainer.factory,
    )
    product_service = ServiceProvider(
        AsyncProductService,
        factory=ServiceContainer.factory,
    )
    event_service = ServiceProvider(
        AsyncEventService,
        factory=ServiceContainer.factory,
    )
    search_service = ServiceProvider(
        AsyncSearchService,
        engine_uri=ServiceContainer.engine_uri,
    )
