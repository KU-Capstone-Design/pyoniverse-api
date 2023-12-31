from dataclasses import asdict
from typing import Any, Literal, Sequence

from chalice import BadRequestError

from chalicelib.business.interface.service import EventServiceIfs
from chalicelib.entity.event import EventEntity
from chalicelib.service.interface.factory import FactoryIfs
from chalicelib.service.interface.service import AbstractService
from chalicelib.business.model.enum import OperatorEnum


class AsyncEventService(EventServiceIfs, AbstractService):
    def __init__(self, factory: FactoryIfs):
        super().__init__(factory)
        self.__rel_name = "events"
        self.__db_name = "service"

    async def find_chunk(
        self, sort_key: str, direction: Literal["asc", "desc"], chunk_size: int
    ) -> Sequence[EventEntity]:
        if not isinstance(sort_key, str):
            raise BadRequestError(f"{sort_key} should be str type")
        if direction not in {"asc", "desc"}:
            raise BadRequestError(f"{direction} should be in ['asc', 'desc']")
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            raise BadRequestError(f"{chunk_size} should be int type and >=0")
        return await self.find_chunk_by(
            filter_key="status",
            filter_value=1,
            sort_key=sort_key,
            direction=direction,
            chunk_size=chunk_size,
        )

    async def find_by_id(self, entity: EventEntity) -> EventEntity:
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = await builder.where(OperatorEnum.EQUAL, "id", entity.id).read()
        return result.get()

    async def find_all_by_brand(self, id: int) -> Sequence[EventEntity]:
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = await builder.where(OperatorEnum.EQUAL, "brand", id).read()
        return result.get()

    async def add_values(self, entity: EventEntity) -> EventEntity:
        """
        filter: {"id": entity.id}
        data: {good_count: ..., view_count: ...}
        해당 값만큼 필드를 증감한다.
        Ex) good_count: 2, prv_good_count: 1 -> cur_good_count: 3
        """
        if not isinstance(entity, EventEntity):
            raise BadRequestError("Entity should be ProductEntity")
        if not isinstance(entity.id, int):
            raise BadRequestError(f"{entity.id} should be int type")
        tmp = asdict(entity)
        data = {}
        for key, val in tmp.items():
            if key in ["good_count", "view_count"] and val is not None:
                data[key] = val

        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = await builder.where(OperatorEnum.EQUAL, "id", entity.id).update(**data)
        return result.get()

    async def find_chunk_by(
        self,
        filter_key: str,
        filter_value: Any,
        sort_key: str,
        direction: Literal["asc", "desc"],
        chunk_size: int = 3,
    ):
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = await (
            builder.where(OperatorEnum.EQUAL, filter_key, filter_value)
            .order(sort_key, direction)
            .limit(chunk_size)
            .read()
        )
        return result.get()
