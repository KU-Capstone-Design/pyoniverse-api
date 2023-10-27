from chalicelib.business.brand.business import AsyncBrandBusiness
from chalicelib.view.brand_view import BrandView
from tests.mock.mock import env


def test_injector(env):
    # given
    from chalicelib.dependency_injector.injector import TmpMainInjector

    main_injector = TmpMainInjector()
    # when
    main_injector.inject()
    # then
    assert isinstance(BrandView.business, AsyncBrandBusiness)
