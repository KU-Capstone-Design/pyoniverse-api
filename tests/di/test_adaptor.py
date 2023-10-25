import pytest

from chalicelib.db.adaptor.mongo import MongoAdaptor
from tests.mock.mock import env


@pytest.fixture
def adaptor_injector(env):
    from chalicelib.di.db.adaptor import DBAdaptorInjector

    injector = DBAdaptorInjector()
    yield injector
    injector.unwire()


def test_repository_injector(adaptor_injector):
    # given
    # adaptor_injector.config.db.mongo_uri.from_env("MONGO_URI")
    # when
    mongo_adaptor = adaptor_injector.mongo_adaptor()
    # then
    assert isinstance(mongo_adaptor, MongoAdaptor)
