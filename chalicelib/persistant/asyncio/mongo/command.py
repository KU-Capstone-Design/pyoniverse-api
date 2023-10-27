import os
from typing import Any, Literal, Sequence

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ReadPreference

from chalicelib.entity.base import EntityType
from chalicelib.entity.util import ENTITY_MAP
from chalicelib.service.interface.command import (
    EqualCommandIfs,
    SelectAllCommandIfs,
    SortByLimit10CommandIfs,
)


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
        result = await self._db[self._rel_name].find_one(
            filter={self._key: self._value}
        )
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
        result = (
            await self._db[self._rel_name]
            .find()
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
        key: str = None,
        value: Any = None,
        db_name: Literal["constant", "service"] = "service",
    ):
        super().__init__(rel_name=rel_name, key=key, value=value, db_name=db_name)
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

    async def execute(self) -> Sequence[EntityType]:
        result = await self._db[self._rel_name].find().to_list(length=None)
        if result:
            return [
                ENTITY_MAP[self._db_name][self._rel_name].from_dict(r) for r in result
            ]
        else:
            return []
