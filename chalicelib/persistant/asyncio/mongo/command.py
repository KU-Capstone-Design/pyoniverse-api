import logging
import os
from typing import Any, Literal, Sequence

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING, ReadPreference

from chalicelib.entity.base import EntityType
from chalicelib.entity.util import ENTITY_MAP
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


logger = logging.getLogger(__name__)


class AsyncMongoEqualCommand(EqualCommandIfs):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        rel_name: str,
        key: str,
        value: Any,
        db_name: Literal["constant", "service"] = "service",
    ):
        super().__init__(rel_name=rel_name, key=key, value=value, db_name=db_name)
        self._client = client

        assert isinstance(self._client, AsyncIOMotorClient)
        assert isinstance(self._rel_name, str)
        assert isinstance(self._key, str)
        assert self._db_name in ["constant", "service"]
        if self._db_name == "service":
            db_name = os.getenv("MONGO_DB")
        else:
            db_name = self._db_name
        self._db: AsyncIOMotorDatabase = self._client.get_database(
            db_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )

    async def execute(self) -> EntityType | None:
        """
        Detail 정보에 접근할 때는 status에 관계없이 정보를 띄운다.
        """
        _filter = {self._key: self._value}
        logger.debug(f"AsyncMongoEqualCommand: [{self._db}.{self._rel_name}] {_filter}")
        result = await self._db[self._rel_name].find_one(filter=_filter)
        if result:
            return ENTITY_MAP[self._db_name][self._rel_name].from_dict(result)
        else:
            return None


class AsyncMongoSortByLimit10Command(SortByLimit10CommandIfs):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        rel_name: str,
        key: str,
        value: Any,
        db_name: Literal["constant", "service"] = "service",
    ):
        super().__init__(rel_name=rel_name, key=key, value=value, db_name=db_name)
        self._client = client

        assert isinstance(self._client, AsyncIOMotorClient)
        assert isinstance(self._rel_name, str)
        assert isinstance(self._key, str)
        assert self._value in [-1, +1]
        assert self._db_name in ["constant", "service"]
        if self._db_name == "service":
            db_name = os.getenv("MONGO_DB")
        else:
            db_name = self._db_name
        self._db: AsyncIOMotorDatabase = self._client.get_database(
            db_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )

    async def execute(self) -> Sequence[EntityType]:
        _filter = {"status": {"$gt": 0}}
        logger.debug(
            f"AsyncMongoSortByLimit10Command: [{self._db}.{self._rel_name}] {_filter}"
        )
        result = (
            await self._db[self._rel_name]
            .find(filter=_filter)
            .sort(self._key, self._value)
            .to_list(10)
        )
        if result:
            return [
                ENTITY_MAP[self._db_name][self._rel_name].from_dict(r) for r in result
            ]
        else:
            return []


class AsyncMongoSelectAllCommand(SelectAllCommandIfs):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        rel_name: str,
        key: str,
        value: Any,
        db_name: Literal["constant", "service"] = "service",
    ):
        super().__init__(rel_name=rel_name, key=key, value=value, db_name=db_name)
        self._client = client

        assert isinstance(self._client, AsyncIOMotorClient)
        assert isinstance(self._rel_name, str)
        assert isinstance(self._key, str)
        assert self._value in [-1, +1]
        assert self._db_name in ["constant", "service"]
        if self._db_name == "service":
            db_name = os.getenv("MONGO_DB")
        else:
            db_name = self._db_name
        self._db: AsyncIOMotorDatabase = self._client.get_database(
            db_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )

    async def execute(self) -> Sequence[EntityType]:
        _filter = {"status": {"$gt": 0}}
        logger.debug(
            f"AsyncMongoSelectAllCommand: [{self._db}.{self._rel_name}] {_filter}"
        )
        result = (
            await self._db[self._rel_name]
            .find(filter=_filter)
            .sort(self._key, self._value)
            .to_list(length=None)
        )
        if result:
            return [
                ENTITY_MAP[self._db_name][self._rel_name].from_dict(r) for r in result
            ]
        else:
            return []


class AsyncMongoSelectAllByCommand(SelectAllByCommandIfs):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        rel_name: str,
        key: str,
        value: Any,
        db_name: Literal["constant", "service"] = "service",
    ):
        super().__init__(rel_name=rel_name, key=key, value=value, db_name=db_name)
        self._client = client

        assert isinstance(self._client, AsyncIOMotorClient)
        assert isinstance(self._rel_name, str)
        assert isinstance(self._key, str)
        assert self._db_name in ["constant", "service"]
        if self._db_name == "service":
            db_name = os.getenv("MONGO_DB")
        else:
            db_name = self._db_name
        self._db: AsyncIOMotorDatabase = self._client.get_database(
            db_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )

    async def execute(self) -> Sequence[EntityType]:
        _filter = {"status": {"$gt": 0}, self._key: self._value}
        logger.debug(
            f"AsyncMongoSelectAllByCommand: [{self._db}.{self._rel_name}] {_filter}"
        )
        result = (
            await self._db[self._rel_name].find(filter=_filter).to_list(length=None)
        )
        if result:
            return [
                ENTITY_MAP[self._db_name][self._rel_name].from_dict(r) for r in result
            ]
        else:
            return []


class AsyncMongoSelectBySortByCommand(SelectBySortByCommandIfs):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        rel_name: str,
        key: str,
        value: Any,
        sort_key: str,
        sort_value: Literal["asc", "desc"],
        chunk_size: int = None,
        db_name: Literal["constant", "service"] = "service",
    ):
        super().__init__(
            rel_name=rel_name,
            key=key,
            value=value,
            db_name=db_name,
            sort_key=sort_key,
            sort_value=sort_value,
            chunk_size=chunk_size,
        )
        self._client = client

        assert isinstance(self._client, AsyncIOMotorClient)
        assert isinstance(self._rel_name, str)
        assert isinstance(self._key, str)
        assert self._db_name in ["constant", "service"]
        if self._db_name == "service":
            db_name = os.getenv("MONGO_DB")
        else:
            db_name = self._db_name
        self._db: AsyncIOMotorDatabase = self._client.get_database(
            db_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )
        assert isinstance(self._sort_key, str)
        assert self._sort_value in {"asc", "desc"}
        if self._sort_value == "asc":
            self._sort_value = 1
        else:
            self._sort_value = -1
        assert isinstance(self._chunk_size, int) or self._chunk_size is None

    async def execute(self) -> Sequence[EntityType] | EntityType | None:
        _filter = {"status": {"$gt": 0}, self._key: self._value}
        logger.debug(
            f"AsyncMongoSelectBySortByCommand: [{self._db}.{self._rel_name}] {_filter}"
        )
        result = (
            await self._db[self._rel_name]
            .find(filter=_filter)
            .sort(self._sort_key, self._sort_value)
            .to_list(self._chunk_size)
        )
        if result:
            return [
                ENTITY_MAP[self._db_name][self._rel_name].from_dict(r) for r in result
            ]
        else:
            return []


class AsyncMongoSelectInSortByCommand(SelectInSortByCommandIfs):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        rel_name: str,
        key: str,
        value: Any,
        sort_key: str,
        sort_value: Literal["asc", "desc"],
        db_name: Literal["constant", "service"] = "service",
    ):
        super().__init__(
            rel_name=rel_name,
            key=key,
            value=value,
            db_name=db_name,
            sort_key=sort_key,
            sort_value=sort_value,
        )
        self._client = client

        assert isinstance(self._client, AsyncIOMotorClient)
        assert isinstance(self._rel_name, str)
        assert isinstance(self._key, str)
        assert isinstance(self._value, list)
        assert self._db_name in ["constant", "service"]
        if self._db_name == "service":
            db_name = os.getenv("MONGO_DB")
        else:
            db_name = self._db_name
        self._db: AsyncIOMotorDatabase = self._client.get_database(
            db_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )
        assert isinstance(self._sort_key, str)
        assert self._sort_value in {"asc", "desc"}
        if self._sort_value == "asc":
            self._sort_value = 1
        else:
            self._sort_value = -1

    async def execute(self) -> Sequence[EntityType] | EntityType | None:
        _filter = {self._key: {"$in": self._value}}
        logger.debug(
            f"AsyncMongoSelectBySortByCommand: [{self._db}.{self._rel_name}] {_filter}"
        )
        result = (
            await self._db[self._rel_name]
            .find(filter=_filter)
            .sort(self._sort_key, self._sort_value)
            .to_list(None)
        )
        if result:
            return [
                ENTITY_MAP[self._db_name][self._rel_name].from_dict(r) for r in result
            ]
        else:
            return []


class AsyncMongoSelectRandomCommand(SelectRandomCommandIfs):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        rel_name: str,
        chunk_size: int,
        db_name: Literal["constant", "service"] = "service",
    ):
        super().__init__(rel_name=rel_name, db_name=db_name, chunk_size=chunk_size)
        self._client = client

        assert isinstance(self._client, AsyncIOMotorClient)
        assert isinstance(self._rel_name, str)
        assert self._db_name in ["constant", "service"]
        if self._db_name == "service":
            db_name = os.getenv("MONGO_DB")
        else:
            db_name = self._db_name
        self._db: AsyncIOMotorDatabase = self._client.get_database(
            db_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )
        assert isinstance(self._chunk_size, int)

    async def execute(self) -> Sequence[EntityType] | EntityType | None:
        pipeline = [{"$sample": {"size": self._chunk_size}}]
        logger.debug(
            f"AsyncMongoSelectRandomCommand: [{self._db}.{self._rel_name}] {pipeline}(pipeline)"
        )
        result = (
            await self._db[self._rel_name].aggregate(pipeline=pipeline).to_list(None)
        )
        if result:
            return [
                ENTITY_MAP[self._db_name][self._rel_name].from_dict(r) for r in result
            ]
        else:
            return []


class AsyncMongoCountByCommand(CountByCommandIfs):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        rel_name: str,
        key: str,
        value: Any,
        db_name: Literal["constant", "service"] = "service",
    ):
        super().__init__(rel_name=rel_name, db_name=db_name, key=key, value=value)
        self._client = client

        assert isinstance(self._client, AsyncIOMotorClient)
        assert isinstance(self._rel_name, str)
        assert self._db_name in ["constant", "service"]
        if self._db_name == "service":
            db_name = os.getenv("MONGO_DB")
        else:
            db_name = self._db_name
        self._db: AsyncIOMotorDatabase = self._client.get_database(
            db_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )

    async def execute(self) -> int:
        if self._key is None:
            length = await self._db[self._rel_name].count_documents(filter={})
        else:
            length = await self._db[self._rel_name].count_documents(
                filter={self._key: self._value}
            )
        return length


class AsyncMongoSelectPageByOrderByCommand(SelectPageByOrderByCommandIfs):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._client = client
        assert isinstance(self._client, AsyncIOMotorClient)
        assert isinstance(self._rel_name, str)
        assert self._db_name in ["constant", "service"]
        if self._db_name == "service":
            db_name = os.getenv("MONGO_DB")
        else:
            db_name = self._db_name
        self._db: AsyncIOMotorDatabase = self._client.get_database(
            db_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )
        assert self._page > 0 and self._page_size > 0
        assert self._sort_direction in ["asc", "desc"]

    async def execute(self) -> Sequence[EntityType] | EntityType | None:
        if isinstance(self._value, list):
            _filter = {self._key: {"$in": self._value}}
        else:
            _filter = {self._key: self._value}

        logger.debug(
            f"AsyncMongoSelectPageByOrderByCommand: [{self._db}.{self._rel_name}] "
            f"filter={_filter}, page={self._page}, page_size={self._page_size}, "
            f"sort_key={self._sort_key}, sort_direction={self._sort_direction}"
        )
        page = self._page - 1
        if self._sort_direction == "asc":
            sort_direction = ASCENDING
        else:
            sort_direction = DESCENDING

        result = await (
            self._db[self._rel_name]
            .find(filter=_filter)
            .sort(self._sort_key, sort_direction)
            .skip(self._page * self._page_size)
            .limit(self._page_size)
            .to_list(None)
        )
        return [ENTITY_MAP[self._db_name][self._rel_name].from_dict(r) for r in result]
