from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Resource

from chalicelib.persistant.mongo.adaptor import MongoAdaptor
from chalicelib.interface.adaptor import DBAdaptor


class DBAdaptorProvider(Resource):
    provided_type = DBAdaptor


class DBAdaptorContainer(DeclarativeContainer):
    pass


class DBAdaptorInjector(DBAdaptorContainer):
    config = Configuration()
    config.db.mongo_uri.from_env("MONGO_URI")
    mongo_adaptor = DBAdaptorProvider(MongoAdaptor, conn_uri=config.db.mongo_uri)
