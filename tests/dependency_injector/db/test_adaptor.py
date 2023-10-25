from chalicelib.db.adaptor.mongo import MongoAdaptor
from tests.dependency_injector.mock.injector import adaptor_injector
from tests.mock.mock import env


def test_adaptor_injector(env, adaptor_injector):
    # when
    mongo_adaptor = adaptor_injector.mongo_adaptor()
    # then
    assert isinstance(mongo_adaptor, MongoAdaptor)
