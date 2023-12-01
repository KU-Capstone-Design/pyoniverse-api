from chalicelib.persistant.refactor.builder import AsyncMongoBuilder
from chalicelib.persistant.refactor.factory import AsyncMongoFactory
from chalicelib.service_refactor.interface.factory import FactoryIfs


def test_async_mongo_factory(mongo_client):
    # given
    factory: FactoryIfs = AsyncMongoFactory(client=mongo_client)
    # when
    builder1 = factory.make(db="test", rel="products")
    builder2 = factory.make(db="test", rel="products")
    # then
    assert isinstance(builder1, AsyncMongoBuilder) and isinstance(
        builder2, AsyncMongoBuilder
    )
    assert builder1 is not builder2
