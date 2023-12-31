from asyncio import AbstractEventLoop

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Dependency, Singleton

from chalicelib.business.brand.business import AsyncBrandBusiness
from chalicelib.business.event.business import AsyncEventBusiness
from chalicelib.business.home.business import AsyncHomeBusiness
from chalicelib.business.interface.business import BusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import (
    ConstantBrandServiceIfs,
    EventServiceIfs,
    ProductServiceIfs,
    SearchServiceIfs,
)
from chalicelib.business.metric.business import AsyncMetricBusiness
from chalicelib.business.product.business import AsyncProductBusiness
from chalicelib.business.search.business import AsyncSearchBusiness


class BusinessProvider(Singleton):
    provided_type = BusinessIfs


class BusinessContainer(DeclarativeContainer):
    # service
    event_service = Dependency(EventServiceIfs)
    product_service = Dependency(ProductServiceIfs)
    constant_brand_service = Dependency(ConstantBrandServiceIfs)
    search_service = Dependency(SearchServiceIfs)
    # converter
    home_converter = Dependency(ConverterIfs)
    event_converter = Dependency(ConverterIfs)
    search_converter = Dependency(ConverterIfs)
    product_converter = Dependency(ConverterIfs)
    metric_converter = Dependency(ConverterIfs)
    brand_converter = Dependency(ConverterIfs)
    # loop
    loop = Dependency(AbstractEventLoop)


class BusinessInjector(BusinessContainer):
    wiring_config = WiringConfiguration(packages=["chalicelib.view"])

    brand_business = BusinessProvider(
        AsyncBrandBusiness,
        constant_brand_service=BusinessContainer.constant_brand_service,
        product_service=BusinessContainer.product_service,
        event_service=BusinessContainer.event_service,
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
        search_service=BusinessContainer.search_service,
        converter=BusinessContainer.search_converter,
        loop=BusinessContainer.loop,
    )
    product_business = BusinessProvider(
        AsyncProductBusiness,
        product_service=BusinessContainer.product_service,
        constant_brand_service=BusinessContainer.constant_brand_service,
        converter=BusinessContainer.product_converter,
        loop=BusinessContainer.loop,
    )
    metric_business = BusinessProvider(
        AsyncMetricBusiness,
        product_service=BusinessContainer.product_service,
        event_service=BusinessContainer.event_service,
        converter=BusinessContainer.metric_converter,
        loop=BusinessContainer.loop,
    )
