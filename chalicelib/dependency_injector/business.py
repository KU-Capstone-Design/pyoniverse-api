from asyncio import AbstractEventLoop

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Dependency, Singleton

from chalicelib.business.brand.business import AsyncBrandBusiness
from chalicelib.business.interface.business import BusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import BrandServiceIfs


class BusinessProvider(Singleton):
    provided_type = BusinessIfs


class BusinessContainer(DeclarativeContainer):
    brand_service = Dependency(BrandServiceIfs)
    brand_converter = Dependency(ConverterIfs)
    loop = Dependency(AbstractEventLoop)


class BusinessInjector(BusinessContainer):
    wiring_config = WiringConfiguration(modules=["chalicelib.view"])

    brand_business = BusinessProvider(
        AsyncBrandBusiness,
        brand_service=BusinessContainer.brand_service,
        converter=BusinessContainer.brand_converter,
        loop=BusinessContainer.loop,
    )
