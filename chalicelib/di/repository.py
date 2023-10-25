from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Dependency, Singleton

from chalicelib.db.adaptor.mongo import MongoAdaptor
from chalicelib.db.brand.repository import BrandMongoRepository
from chalicelib.db.event.repository import EventMongoRepository
from chalicelib.db.home.repository import HomeMongoRepository
from chalicelib.db.interface.adaptor import DBAdaptor
from chalicelib.db.product.repository import ProductMongoRepository
from chalicelib.interface.repository import Repository


class DBAdaptorProvider(Singleton):
    provided_type = DBAdaptor


class DBAdaptorContainer(DeclarativeContainer):
    # provider_type = DBAdaptorProvider
    wiring_config = WiringConfiguration(packages=["chalicelib.db.adaptor"])


class DBAdaptorInjector(DBAdaptorContainer):
    config = Configuration()
    mongo_adaptor = DBAdaptorProvider(MongoAdaptor, conn_uri=config.db.mongo_uri)


class RepositoryProvider(Singleton):
    provided_type = Repository


class RepositoryContainer(DeclarativeContainer):
    # provider_type = RepositoryProvider
    adaptor = Dependency(instance_of=DBAdaptor)
    config = Configuration()
    wiring_config = WiringConfiguration(packages=["chalicelib.db"])


class RepositoryInjector(RepositoryContainer):
    brand_repository = RepositoryProvider(BrandMongoRepository)
    home_repository = RepositoryProvider(HomeMongoRepository)
    product_repository = RepositoryProvider(ProductMongoRepository)
    event_repository = RepositoryProvider(EventMongoRepository)
