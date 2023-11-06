from dataclasses import asdict
from typing import Any, Literal, Sequence

from chalice import BadRequestError, NotFoundError

from chalicelib.business.interface.service import EventServiceIfs
from chalicelib.entity.event import EventEntity
from chalicelib.service.interface.command_factory import CommandFactoryIfs
from chalicelib.service.interface.invoker import InvokerIfs


class AsyncEventService(EventServiceIfs):
    def __init__(self, invoker: InvokerIfs, command_factory: CommandFactoryIfs):
        self.__invoker = invoker
        self.__command_factory = command_factory
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

        if chunk_size <= 10:
            self.__invoker.add_command(
                self.__command_factory.get_sort_by_limit10_command(
                    db_name=self.__db_name,
                    rel_name=self.__rel_name,
                    key=sort_key,
                    value=1 if direction == "asc" else -1,
                )
            )
        else:
            self.__invoker.add_command(
                self.__command_factory.get_select_all_command(
                    db_name=self.__db_name,
                    rel_name=self.__rel_name,
                    key=sort_key,
                    value=1 if direction == "asc" else -1,
                )
            )
        result = (await self.__invoker.invoke())[0]
        if not result:
            raise NotFoundError(f"{self.__db_name}.{self.__rel_name} is empty")
        else:
            return result[:chunk_size]

    async def find_by_id(self, entity: EventEntity) -> EventEntity:
        self.__invoker.add_command(
            self.__command_factory.get_equal_command(
                db_name=self.__db_name,
                rel_name=self.__rel_name,
                key="id",
                value=entity.id,
            )
        )
        result = (await self.__invoker.invoke())[0]
        if not result:
            raise NotFoundError(
                f"id={entity.id} not in {self.__db_name}.{self.__rel_name}"
            )
        else:
            return result

    async def find_all_by_brand(self, id: int) -> Sequence[EventEntity]:
        self.__invoker.add_command(
            self.__command_factory.get_select_all_by_command(
                db_name=self.__db_name, rel_name=self.__rel_name, key="brand", value=id
            )
        )
        result = (await self.__invoker.invoke())[0]
        if not result:
            raise NotFoundError(f"brand={id} not in {self.__db_name}.{self.__rel_name}")
        else:
            return result

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

        # find prv count - committed value가 아닐 수 있다.
        self.__invoker.add_command(
            self.__command_factory.get_equal_command(
                db_name=self.__db_name,
                rel_name=self.__rel_name,
                key="id",
                value=entity.id,
            )
        )
        result: EventEntity = (await self.__invoker.invoke())[0]
        if not result:
            raise NotFoundError(
                f"{entity.id} not in {self.__db_name}.{self.__rel_name}"
            )
        # add value
        self.__invoker.add_command(
            self.__command_factory.get_add_modify_equal_command(
                db_name=self.__db_name,
                rel_name=self.__rel_name,
                key="id",
                value=entity.id,
                data=data,
            )
        )
        await self.__invoker.invoke()

        # 이 값은 실제 DB에 업데이트 된 값과 다를 수 있다(다른 유저가 동시에 요청한 경우)
        if "good_count" in data:
            result.good_count += data["good_count"]
        if "view_count" in data:
            result.view_count += data["view_count"]
        return result

    async def find_chunk_by(
        self,
        filter_key: str,
        filter_value: Any,
        sort_key: str,
        direction: Literal["asc", "desc"],
        chunk_size: int,
    ):
        self.__invoker.add_command(
            self.__command_factory.get_select_by_sort_by_command(
                db_name=self.__db_name,
                rel_name=self.__rel_name,
                key=filter_key,
                value=filter_value,
                sort_key="good_count",
                sort_value="desc",
                chunk_size=3,
            )
        )
        result = (await self.__invoker.invoke())[0]
        if not result:
            raise NotFoundError(f"brand={id} not in {self.__db_name}.{self.__rel_name}")
        else:
            return result
