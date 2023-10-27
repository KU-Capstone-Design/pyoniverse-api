from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from chalicelib.business.interface.service import ServiceIfs
from chalicelib.service.brand.service import AsyncBrandService
from chalicelib.service.constant_brand.service import AsyncConstantBrandService
from chalicelib.service.event.service import AsyncEventService
from chalicelib.service.interface.command_factory import CommandFactoryIfs
from chalicelib.service.interface.invoker import InvokerIfs
from chalicelib.service.product.service import AsyncProductService


class ServiceProvider(Singleton):
    provided_type = ServiceIfs


class ServiceContainer(DeclarativeContainer):
    command_factory = Dependency(CommandFactoryIfs)
    brand_invoker = Dependency(InvokerIfs)
    constant_brand_invoker = Dependency(InvokerIfs)
    product_invoker = Dependency(InvokerIfs)
    event_invoker = Dependency(InvokerIfs)


class ServiceInjector(ServiceContainer):
    brand_service = ServiceProvider(
        AsyncBrandService,
        invoker=ServiceContainer.brand_invoker,
        command_factory=ServiceContainer.command_factory,
    )
    constant_brand_service = ServiceProvider(
        AsyncConstantBrandService,
        invoker=ServiceContainer.constant_brand_invoker,
        command_factory=ServiceContainer.command_factory,
    )
    product_service = ServiceProvider(
        AsyncProductService,
        invoker=ServiceContainer.product_invoker,
        command_factory=ServiceContainer.command_factory,
    )
    event_service = ServiceProvider(
        AsyncEventService,
        invoker=ServiceContainer.event_invoker,
        command_factory=ServiceContainer.command_factory,
    )
