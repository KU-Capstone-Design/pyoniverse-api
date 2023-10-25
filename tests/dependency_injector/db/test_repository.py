from chalicelib.db.mongo.brand_repository import BrandMongoRepository
from chalicelib.db.mongo.event_repository import EventMongoRepository
from chalicelib.db.mongo.home_repository import HomeMongoRepository
from chalicelib.db.mongo.product_repository import ProductMongoRepository
from tests.dependency_injector.mock.injector import (
    adaptor_injector,
    repository_injector,
)
from tests.mock.mock import env


def test_repository_dependency(env, adaptor_injector):
    from chalicelib.dependency_injector.db.repository import RepositoryInjector

    # given
    repository_injector = RepositoryInjector(adaptor=adaptor_injector.mongo_adaptor())
    # when & then
    try:
        repository_injector.check_dependencies()
    except Exception:
        assert False
    else:
        assert True


def test_repository_injector(env, repository_injector):
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
