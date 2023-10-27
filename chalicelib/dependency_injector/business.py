# from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
# from dependency_injector.providers import Dependency, Singleton
#
# from chalicelib.business.brand.business import AsyncBrandBusiness
# from chalicelib.business.brand.converter import BrandConverter
# from chalicelib.business.interface.business import BusinessIfs
# from chalicelib.business.interface.service import BrandServiceIfs
# from chalicelib.domain.brand.brand_service import BrandService
# from chalicelib.domain.event.event_service import EventService
# from chalicelib.domain.home.home_service import HomeService
# from chalicelib.domain.product.product_service import ProductService
# from chalicelib.interface.repository import Repository
# from chalicelib.interface.service import Service
#
#
# class BusinessProvider(Singleton):
#     provided_type = BusinessIfs
#
#
# class BusinessContainer(DeclarativeContainer):
#     brand_service = Dependency(BrandServiceIfs)
#
#
# class BusinessInjector(BusinessContainer):
#     # in-class wiring_config는 현재 class의 provider에만 적용된다.
#     wiring_config = WiringConfiguration(packages=["chalicelib.view"])
#     brand_business = BusinessProvider(
#             AsyncBrandBusiness,
#             brand_service=BusinessContainer.brand_service,
#             converter=BrandConverter(),
#             loop=
#     )
#     home_service = ServiceProvider(
#         HomeService, repository=ServiceContainer.home_repository
#     )
#     brand_service = ServiceProvider(
#         BrandService, repository=ServiceContainer.brand_repository
#     )
#     product_service = ServiceProvider(
#         ProductService, repository=ServiceContainer.product_repository
#     )
#     event_service = ServiceProvider(
#         EventService, repository=ServiceContainer.event_repository
#     )
