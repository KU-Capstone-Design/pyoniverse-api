from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.persistant.asyncio.mongo.command import (
    AsyncMongoEqualCommand,
    AsyncMongoSelectAllCommand,
    AsyncMongoSortByLimit10Command,
)
from chalicelib.service.interface.command import (
    EqualCommandIfs,
    SelectAllCommandIfs,
    SortByLimit10CommandIfs,
)
from chalicelib.service.interface.command_factory import CommandFactoryIfs


class AsyncMongoCommandFactory(CommandFactoryIfs):
    def __init__(self, client: AsyncIOMotorClient):
        self.__client = client

    def get_equal_command(
        self, db_name: str, rel_name: str, key: str, value: Any
    ) -> EqualCommandIfs:
        return AsyncMongoEqualCommand(
            client=self.__client,
            db_name=db_name,
            rel_name=rel_name,
            key=key,
            value=value,
        )

    def get_sort_by_limit10_command(
        self, db_name: str, rel_name: str, key: str, value: Any
    ) -> SortByLimit10CommandIfs:
        return AsyncMongoSortByLimit10Command(
            client=self.__client,
            db_name=db_name,
            rel_name=rel_name,
            key=key,
            value=value,
        )

    def get_select_all_command(
        self, db_name: str, rel_name: str, key: str, value: Any
    ) -> SelectAllCommandIfs:
        return AsyncMongoSelectAllCommand(
            client=self.__client,
            db_name=db_name,
            rel_name=rel_name,
            key=key,
            value=value,
        )
