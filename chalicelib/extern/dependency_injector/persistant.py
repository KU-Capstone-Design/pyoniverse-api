from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory, Singleton
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.persistant.asyncio.invoker import AsyncInvoker
from chalicelib.persistant.asyncio.mongo.command_factory import AsyncMongoCommandFactory


class PersistentInjector(DeclarativeContainer):
    client: AsyncIOMotorClient = Dependency(AsyncIOMotorClient)
    invoker = Factory(AsyncInvoker)  # invoker는 commands를 저장하므로 각 Service마다 달라야 한다.
    command_factory = Singleton(AsyncMongoCommandFactory, client=client)
