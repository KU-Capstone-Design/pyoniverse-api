from chalicelib.domain.brand.brand_controller import BrandController
from chalicelib.domain.brand.brand_service import BrandService
from chalicelib.domain.event.event_controller import EventController
from chalicelib.domain.event.event_service import EventService
from chalicelib.domain.home.home_controller import HomeController
from chalicelib.domain.home.home_service import HomeService
from tests.mock.mock import env


def test_injector(env):
    # given
    from chalicelib.dependency_injector.injector import MainInjector

    main_injector = MainInjector()
    # when
    main_injector.inject()
    # then
    assert isinstance(BrandController.service, BrandService)
    assert isinstance(HomeController.service, HomeService)
    assert isinstance(EventController.service, EventService)
