from tests.di.mock.injector import repository_injector, adaptor_injector
from tests.mock.mock import env


def test_service_dependency(env, adaptor_injector, repository_injector):
    from chalicelib.di.service.service import ServiceInjector

    # given
    repository_injector = ServiceInjector(
        home_repository=repository_injector.home_repository(),
        brand_repository=repository_injector.brand_repository(),
        event_repository=repository_injector.event_repository(),
        product_repository=repository_injector.product_repository(),
    )
    # when & then
    try:
        repository_injector.check_dependencies()
    except Exception:
        assert False
    else:
        assert True
