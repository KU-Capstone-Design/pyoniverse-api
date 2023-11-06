from typing import Any, Literal

import boto3
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.persistant.asyncio.mongo.command import (
    AsyncMongoEqualCommand,
    AsyncMongoSelectAllByCommand,
    AsyncMongoSelectAllCommand,
    AsyncMongoSelectBySortByCommand,
    AsyncMongoSortByLimit10Command,
)
from chalicelib.persistant.asyncio.sqs.command import AsyncSqsAddModifyEqualCommand
from chalicelib.service.interface.command import (
    EqualCommandIfs,
    SelectAllByCommandIfs,
    SelectAllCommandIfs,
    SelectBySortByCommandIfs,
    SortByLimit10CommandIfs,
)
from chalicelib.service.interface.command_factory import CommandFactoryIfs


class AsyncCommandFactory(CommandFactoryIfs):
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

    def get_select_all_by_command(
        self,
        db_name: str,
        rel_name: str,
        key: str,
        value: Any,
    ) -> SelectAllByCommandIfs:
        return AsyncMongoSelectAllByCommand(
            client=self.__client,
            db_name=db_name,
            rel_name=rel_name,
            key=key,
            value=value,
        )

    def get_add_modify_equal_command(
        self, db_name: str, rel_name: str, key: str, value: Any, data: dict
    ) -> AsyncSqsAddModifyEqualCommand:
        return AsyncSqsAddModifyEqualCommand(
            client=boto3.client("sqs"),
            db_name=db_name,
            rel_name=rel_name,
            key=key,
            value=value,
            data=data,
        )

    def get_select_by_sort_by_command(
        self,
        db_name: str,
        rel_name: str,
        key: str,
        value: Any,
        sort_key: str,
        sort_value: Literal["asc", "desc"],
        chunk_size: int = None,
    ) -> SelectBySortByCommandIfs:
        return AsyncMongoSelectBySortByCommand(
            client=self.__client,
            db_name=db_name,
            rel_name=rel_name,
            key=key,
            value=value,
            sort_key=sort_key,
            sort_value=sort_value,
            chunk_size=chunk_size,
        )
