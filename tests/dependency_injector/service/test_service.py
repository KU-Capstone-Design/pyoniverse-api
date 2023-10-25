from chalicelib.domain.brand.brand_service import BrandService
from chalicelib.domain.event.event_service import EventService
from chalicelib.domain.home.home_service import HomeService
from chalicelib.domain.product.product_service import ProductService
from tests.dependency_injector.mock.injector import (
    adaptor_injector,
    repository_injector,
    service_injector,
)
from tests.mock.mock import env


def test_service_dependency(env, adaptor_injector, repository_injector):
    from chalicelib.dependency_injector.service.service import ServiceInjector

    # given
    service_injector = ServiceInjector(
        home_repository=repository_injector.home_repository(),
        brand_repository=repository_injector.brand_repository(),
        event_repository=repository_injector.event_repository(),
        product_repository=repository_injector.product_repository(),
    )
    # when & then
    try:
        service_injector.check_dependencies()
    except Exception:
        assert False
    else:
        assert True


def test_service_injector(service_injector):
    # given
    brand_service = service_injector.brand_service()
    event_service = service_injector.event_service()
    home_service = service_injector.home_service()
    product_service = service_injector.product_service()

    # then
    assert isinstance(brand_service, BrandService)
    assert isinstance(event_service, EventService)
    assert isinstance(home_service, HomeService)
    assert isinstance(product_service, ProductService)
