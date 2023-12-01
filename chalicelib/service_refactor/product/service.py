from dataclasses import asdict
from typing import Any, Literal, Sequence

from chalice import BadRequestError, NotFoundError

from chalicelib.business.interface.service import ProductServiceIfs
from chalicelib.entity.event import EventEntity
from chalicelib.entity.product import ProductEntity
from chalicelib.service.interface.command_factory import CommandFactoryIfs
from chalicelib.service.interface.invoker import InvokerIfs


class AsyncProductService(ProductServiceIfs):
    def __init__(self, invoker: InvokerIfs, command_factory: CommandFactoryIfs):
        self.__invoker = invoker
        self.__command_factory = command_factory
        self.__rel_name = "products"
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

    async def find_one(self, entity: ProductEntity) -> ProductEntity:
        if not isinstance(entity, ProductEntity):
            raise BadRequestError("Entity should be ProductEntity")
        if not isinstance(entity.id, int):
            raise BadRequestError(f"{entity.id} should be int type")
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
                f"{entity.id} not in {self.__db_name}.{self.__rel_name}"
            )
        else:
            return result

    async def add_values(self, entity: ProductEntity) -> ProductEntity:
        """
        filter: {"id": entity.id}
        data: {good_count: ..., view_count: ...}
        해당 값만큼 필드를 증감한다.
        Ex) good_count: 2, prv_good_count: 1 -> cur_good_count: 3
        """
        if not isinstance(entity, ProductEntity):
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
        result: ProductEntity = (await self.__invoker.invoke())[0]
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
        filter_value: str,
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
                sort_key=sort_key,
                sort_value=direction,
                chunk_size=3,
            )
        )
        result = (await self.__invoker.invoke())[0]
        if not result:
            raise NotFoundError(
                f"brands.id={id} not in {self.__db_name}.{self.__rel_name}"
            )
        else:
            return result

    async def find_in_sort_by(
        self,
        filter_key: str,
        filter_value: list,
        sort_key: str,
        direction: Literal["asc", "desc"],
    ):
        self.__invoker.add_command(
            self.__command_factory.get_select_in_sort_by_command(
                db_name=self.__db_name,
                rel_name=self.__rel_name,
                key=filter_key,
                value=filter_value,
                sort_key=sort_key,
                sort_value=direction,
            )
        )
        result = (await self.__invoker.invoke())[0]
        if not result:
            raise NotFoundError(
                f"{filter_key} in {filter_value} not in {self.__db_name}.{self.__rel_name}"
            )
        else:
            return result

    async def random(
        self,
        chunk_size: int,
    ):
        self.__invoker.add_command(
            self.__command_factory.get_select_random_command(
                db_name=self.__db_name,
                rel_name=self.__rel_name,
                chunk_size=chunk_size,
            )
        )
        result = (await self.__invoker.invoke())[0]
        if not result:
            raise NotFoundError(f"{self.__db_name}.{self.__rel_name} is empty")
        else:
            return result

    async def get_length(self, filter_key: str = None, filter_value: Any = None) -> int:
        self.__invoker.add_command(
            self.__command_factory.get_count_by_command(
                db_name=self.__db_name,
                rel_name=self.__rel_name,
                key=filter_key,
                value=filter_value,
            )
        )
        result = (await self.__invoker.invoke())[0]
        return result

    async def find_page(
        self,
        filter_key: str,
        filter_value: Any,
        sort_key: str,
        sort_direction: Literal["asc", "desc"],
        page: int,
        page_size: int,
    ):
        self.__invoker.add_command(
            self.__command_factory.get_find_page_command(
                db_name=self.__db_name,
                rel_name=self.__rel_name,
                key=filter_key,
                value=filter_value,
                sort_key=sort_key,
                sort_direction=sort_direction,
                page=page,
                page_size=page_size,
            )
        )
        result = (await self.__invoker.invoke())[0]
        return result