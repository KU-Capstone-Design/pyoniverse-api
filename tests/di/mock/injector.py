import pytest

from tests.mock.mock import env


@pytest.fixture
def adaptor_injector(env):
    from chalicelib.di.db.adaptor import DBAdaptorInjector

    injector = DBAdaptorInjector()
    yield injector


@pytest.fixture
def repository_injector(adaptor_injector):
    from chalicelib.di.db.repository import RepositoryInjector

    injector = RepositoryInjector(adaptor=adaptor_injector.mongo_adaptor())
    yield injector


@pytest.fixture
def service_injector(repository_injector):
    from chalicelib.di.service.service import ServiceInjector

    injector = ServiceInjector(
        home_repository=repository_injector.home_repository(),
        brand_repository=repository_injector.brand_repository(),
        event_repository=repository_injector.event_repository(),
        product_repository=repository_injector.product_repository(),
    )
    yield injector
