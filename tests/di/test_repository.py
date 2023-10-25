import pytest

from chalicelib.db.brand.repository import BrandMongoRepository
from chalicelib.db.event.repository import EventMongoRepository
from chalicelib.db.home.repository import HomeMongoRepository
from chalicelib.db.product.repository import ProductMongoRepository
from tests.mock.mock import env


@pytest.fixture
def adaptor_injector(env):
    from chalicelib.di.db.adaptor import DBAdaptorInjector

    injector = DBAdaptorInjector()
    yield injector
    injector.unwire()


@pytest.fixture
def repository_injector(adaptor_injector):
    from chalicelib.di.db.repository import RepositoryInjector

    injector = RepositoryInjector(adaptor=adaptor_injector.mongo_adaptor())
    yield injector
    injector.unwire()


def test_repository_dependency(adaptor_injector):
    from chalicelib.di.db.repository import RepositoryInjector

    # given
    repository_injector = RepositoryInjector(adaptor=adaptor_injector.mongo_adaptor())
    # when & then
    try:
        repository_injector.check_dependencies()
    except Exception:
        assert False
    else:
        assert True


def test_repository_injector(repository_injector):
    # given
    brand_repository = repository_injector.brand_repository()
    event_repository = repository_injector.event_repository()
    home_repository = repository_injector.home_repository()
    product_repository = repository_injector.product_repository()

    # then
    assert isinstance(brand_repository, BrandMongoRepository)
    assert isinstance(event_repository, EventMongoRepository)
    assert isinstance(home_repository, HomeMongoRepository)
    assert isinstance(product_repository, ProductMongoRepository)
