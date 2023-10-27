from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from chalicelib.business.interface.service import ServiceIfs
from chalicelib.service.brand.service import AsyncBrandService
from chalicelib.service.interface.command_factory import CommandFactoryIfs
from chalicelib.service.interface.invoker import InvokerIfs


class ServiceProvider(Singleton):
    provided_type = ServiceIfs


class ServiceContainer(DeclarativeContainer):
    command_factory = Dependency(CommandFactoryIfs)
    invoker = Dependency(InvokerIfs)


class ServiceInjector(ServiceContainer):
    brand_service = ServiceProvider(
        AsyncBrandService,
        invoker=ServiceContainer.invoker,
        command_factory=ServiceContainer.command_factory,
    )
