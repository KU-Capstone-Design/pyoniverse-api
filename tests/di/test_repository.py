import pytest
from dependency_injector.wiring import Provide

from chalicelib.db.brand.repository import BrandMongoRepository
from chalicelib.db.event.repository import EventMongoRepository
from chalicelib.db.home.repository import HomeMongoRepository
from chalicelib.db.product.repository import ProductMongoRepository
from tests.mock.mock import env


@pytest.fixture
def repository_injector(env):
    from chalicelib.di.repository import RepositoryInjector

    injector = RepositoryInjector()
    yield injector
    injector.unwire()


def test_repository_injector(repository_injector):
    # given
    brand_repository = Provide["brand"]
    event_repository = Provide["event"]
    home_repository = Provide["home"]
    product_repository = Provide["product"]

    # when
    repository_injector.wire()
    # then
    assert isinstance(brand_repository, BrandMongoRepository)
    assert isinstance(event_repository, EventMongoRepository)
    assert isinstance(home_repository, HomeMongoRepository)
    assert isinstance(product_repository, ProductMongoRepository)
