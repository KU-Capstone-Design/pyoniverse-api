from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Dependency, Singleton

from chalicelib.db.brand.repository import BrandMongoRepository
from chalicelib.db.event.repository import EventMongoRepository
from chalicelib.db.home.repository import HomeMongoRepository
from chalicelib.interface.adaptor import DBAdaptor
from chalicelib.db.product.repository import ProductMongoRepository
from chalicelib.interface.repository import Repository


class RepositoryProvider(Singleton):
    provided_type = Repository


class RepositoryContainer(DeclarativeContainer):
    adaptor = Dependency(instance_of=DBAdaptor)
    wiring_config = WiringConfiguration(packages=["chalicelib.db"])


class RepositoryInjector(RepositoryContainer):
    brand_repository = RepositoryProvider(
        BrandMongoRepository, adaptor=RepositoryContainer.adaptor
    )
    home_repository = RepositoryProvider(
        HomeMongoRepository, adaptor=RepositoryContainer.adaptor
    )
    product_repository = RepositoryProvider(
        ProductMongoRepository, adaptor=RepositoryContainer.adaptor
    )
    event_repository = RepositoryProvider(
        EventMongoRepository, adaptor=RepositoryContainer.adaptor
    )
