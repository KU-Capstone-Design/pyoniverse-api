from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.persistant.asyncio.mongo.command import AsyncMongoEqualCommand
from chalicelib.service.interface.command import EqualCommandIfs
from chalicelib.service.interface.command_factory import CommandFactoryIfs


class AsyncMongoCommandFactory(CommandFactoryIfs):
    def __init__(self, client: AsyncIOMotorClient):
        self.__client = client

    def get_equal_command(self, rel_name: str, key: str, value: Any) -> EqualCommandIfs:
        return AsyncMongoEqualCommand(
            client=self.__client, rel_name=rel_name, key=key, value=value
        )
