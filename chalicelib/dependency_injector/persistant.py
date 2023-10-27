from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.mongo.command_factory import AsyncMongoCommandFactory


class PersistentInjector(DeclarativeContainer):
    client: AsyncIOMotorClient = Dependency(AsyncIOMotorClient)
    invoker = Singleton(AsyncInvoker)
    command_factory = Singleton(AsyncMongoCommandFactory, client=client)
