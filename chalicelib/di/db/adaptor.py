from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Singleton

from chalicelib.db.adaptor.mongo import MongoAdaptor
from chalicelib.db.interface.adaptor import DBAdaptor


class DBAdaptorProvider(Singleton):
    provided_type = DBAdaptor


class DBAdaptorContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["chalicelib.db.adaptor"])


class DBAdaptorInjector(DBAdaptorContainer):
    config = Configuration()
    config.db.mongo_uri.from_env("MONGO_URI")
    mongo_adaptor = DBAdaptorProvider(MongoAdaptor, conn_uri=config.db.mongo_uri)
