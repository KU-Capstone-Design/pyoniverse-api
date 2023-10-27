from chalicelib.business.brand.business import AsyncBrandBusiness
from chalicelib.view.brand_view import BrandView
from tests.mock.mock import env


def test_injector(env):
    # given
    from chalicelib.extern.dependency_injector.injector import MainInjector

    main_injector = MainInjector()
    # when
    main_injector.inject()
    # then
    assert isinstance(BrandView.business, AsyncBrandBusiness)
