from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.persistant.refactor.factory import AsyncMongoFactory


class PersistentInjector(DeclarativeContainer):
    client: AsyncIOMotorClient = Dependency(AsyncIOMotorClient)
    factory = Singleton(AsyncMongoFactory, client=client)
