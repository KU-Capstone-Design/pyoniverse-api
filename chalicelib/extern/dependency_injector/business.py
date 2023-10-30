from asyncio import AbstractEventLoop

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Dependency, Singleton

from chalicelib.business.brand.business import AsyncBrandBusiness
from chalicelib.business.event.business import AsyncEventBusiness
from chalicelib.business.home.business import AsyncHomeBusiness
from chalicelib.business.interface.business import BusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import (
    BrandServiceIfs,
    ConstantBrandServiceIfs,
    EventServiceIfs,
    ProductServiceIfs,
)
from chalicelib.business.search.business import AsyncSearchBusiness


class BusinessProvider(Singleton):
    provided_type = BusinessIfs


class BusinessContainer(DeclarativeContainer):
    # service
    brand_service = Dependency(BrandServiceIfs)
    event_service = Dependency(EventServiceIfs)
    product_service = Dependency(ProductServiceIfs)
    constant_brand_service = Dependency(ConstantBrandServiceIfs)
    # converter
    brand_converter = Dependency(ConverterIfs)
    home_converter = Dependency(ConverterIfs)
    event_converter = Dependency(ConverterIfs)
    search_converter = Dependency(ConverterIfs)
    # loop
    loop = Dependency(AbstractEventLoop)


class BusinessInjector(BusinessContainer):
    wiring_config = WiringConfiguration(packages=["chalicelib.view"])

    brand_business = BusinessProvider(
        AsyncBrandBusiness,
        brand_service=BusinessContainer.brand_service,
        converter=BusinessContainer.brand_converter,
        loop=BusinessContainer.loop,
    )
    home_business = BusinessProvider(
        AsyncHomeBusiness,
        constant_brand_service=BusinessContainer.constant_brand_service,
        event_service=BusinessContainer.event_service,
        product_service=BusinessContainer.product_service,
        converter=BusinessContainer.home_converter,
        loop=BusinessContainer.loop,
    )
    event_business = BusinessProvider(
        AsyncEventBusiness,
        event_service=BusinessContainer.event_service,
        constant_brand_service=BusinessContainer.constant_brand_service,
        converter=BusinessContainer.event_converter,
        loop=BusinessContainer.loop,
    )
    search_business = BusinessProvider(
        AsyncSearchBusiness,
        constant_brand_service=BusinessContainer.constant_brand_service,
        product_service=BusinessContainer.product_service,
        converter=BusinessContainer.search_converter,
        loop=BusinessContainer.loop,
    )
