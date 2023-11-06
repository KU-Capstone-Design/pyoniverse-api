import logging
import os
from typing import Any, Literal, Sequence

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ReadPreference

from chalicelib.entity.base import EntityType
from chalicelib.entity.util import ENTITY_MAP
from chalicelib.service.interface.command import (
    EqualCommandIfs,
    SelectAllByCommandIfs,
    SelectAllCommandIfs,
    SelectBySortByCommandIfs,
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
        logger.debug(f"AsyncMongoEqualCommand: {_filter}")
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
        logger.debug(f"AsyncMongoSortByLimit10Command: {_filter}")
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
        logger.debug(f"AsyncMongoSelectAllCommand: {_filter}")
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
        logger.debug(f"AsyncMongoSelectAllByCommand: {_filter}")
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
        logger.debug(f"AsyncMongoSelectBySortByCommand: {_filter}")
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
