from typing import Any, Literal

import boto3
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.persistant.asyncio.mongo.command import (
    AsyncMongoCountByCommand,
    AsyncMongoEqualCommand,
    AsyncMongoSelectAllByCommand,
    AsyncMongoSelectAllCommand,
    AsyncMongoSelectBySortByCommand,
    AsyncMongoSelectInSortByCommand,
    AsyncMongoSelectPageByOrderByCommand,
    AsyncMongoSelectRandomCommand,
    AsyncMongoSortByLimit10Command,
)
from chalicelib.persistant.asyncio.sqs.command import AsyncSqsAddModifyEqualCommand
from chalicelib.service.interface.command import (
    CountByCommandIfs,
    EqualCommandIfs,
    SelectAllByCommandIfs,
    SelectAllCommandIfs,
    SelectBySortByCommandIfs,
    SelectInSortByCommandIfs,
    SelectPageByOrderByCommandIfs,
    SelectRandomCommandIfs,
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

    def get_select_in_sort_by_command(
        self,
        db_name: str,
        rel_name: str,
        key: str,
        value: list,
        sort_key: str,
        sort_value: Literal["asc", "desc"],
    ) -> SelectInSortByCommandIfs:
        return AsyncMongoSelectInSortByCommand(
            client=self.__client,
            db_name=db_name,
            rel_name=rel_name,
            key=key,
            value=value,
            sort_key=sort_key,
            sort_value=sort_value,
        )

    def get_select_random_command(
        self,
        db_name: str,
        rel_name: str,
        chunk_size: int,
    ) -> SelectRandomCommandIfs:
        return AsyncMongoSelectRandomCommand(
            client=self.__client,
            db_name=db_name,
            rel_name=rel_name,
            chunk_size=chunk_size,
        )

    def get_count_by_command(
        self, db_name: str, rel_name: str, key: str = None, value: Any = None
    ) -> CountByCommandIfs:
        return AsyncMongoCountByCommand(
            client=self.__client,
            db_name=db_name,
            rel_name=rel_name,
            key=key,
            value=value,
        )

    def get_find_page_command(
        self,
        db_name: str,
        rel_name: str,
        key: str,
        value: Any,
        sort_key: str,
        sort_direction: Literal["asc", "desc"],
        page: int,
        page_size: int,
    ) -> SelectPageByOrderByCommandIfs:
        return AsyncMongoSelectPageByOrderByCommand(
            client=self.__client,
            db_name=db_name,
            rel_name=rel_name,
            key=key,
            value=value,
            sort_key=sort_key,
            sort_direction=sort_direction,
            page=page,
            page_size=page_size,
        )
