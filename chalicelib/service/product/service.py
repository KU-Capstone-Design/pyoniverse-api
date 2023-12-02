from dataclasses import asdict
from typing import Any, List, Literal, Sequence

from chalice import BadRequestError

from chalicelib.business.interface.service import ProductServiceIfs
from chalicelib.business.model.enum import OperatorEnum
from chalicelib.entity.event import EventEntity
from chalicelib.entity.product import ProductEntity
from chalicelib.service.interface.factory import FactoryIfs
from chalicelib.service.interface.service import AbstractService


class AsyncProductService(ProductServiceIfs, AbstractService):
    def __init__(self, factory: FactoryIfs):
        super().__init__(factory)
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
        return await self.find_chunk_by(
            filter_key="status",
            filter_value=1,
            sort_key=sort_key,
            direction=direction,
            chunk_size=chunk_size,
        )

    async def find_one(self, entity: ProductEntity) -> ProductEntity:
        if not isinstance(entity, ProductEntity):
            raise BadRequestError("Entity should be ProductEntity")
        if not isinstance(entity.id, int):
            raise BadRequestError(f"{entity.id} should be int type")
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = await builder.where(OperatorEnum.EQUAL, "id", entity.id).read()
        return result.get()

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
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = await builder.where(OperatorEnum.EQUAL, "id", entity.id).update(**data)
        return result.get()

    async def find_chunk_by(
        self,
        filter_key: str,
        filter_value: Any,
        sort_key: str,
        direction: Literal["asc", "desc"],
        chunk_size: int,
    ):
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = (
            await builder.where(OperatorEnum.EQUAL, filter_key, filter_value)
            .order(sort_key, direction)
            .limit(chunk_size)
            .read()
        )
        return result.get()

    async def find_in_sort_by(
        self,
        filter_key: str,
        filter_value: list,
        sort_key: str,
        direction: Literal["asc", "desc"],
    ):
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = (
            await builder.where(OperatorEnum.IN, filter_key, filter_value)
            .order(sort_key, direction)
            .read()
        )
        return result.get()

    async def random(
        self,
        chunk_size: int,
    ):
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = await builder.where(OperatorEnum.EQUAL, "status", 1).random(chunk_size)
        return result.get()

    async def get_length(self, filter_key: str = None, filter_value: Any = None) -> int:
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = await builder.where(
            OperatorEnum.EQUAL, filter_key, filter_value
        ).count()
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
        assert page >= 1
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = await (
            builder.where(OperatorEnum.IN, filter_key, filter_value)
            .order(sort_key, sort_direction)
            .skip((page - 1) * page_size)
            .limit(page_size)
            .read()
        )
        return result.get()

    async def search(
        self,
        queries: List[list],
        sort_key: str,
        direction: Literal["asc", "desc"],
        page: int,
        page_size: int,
    ) -> List[ProductEntity]:
        assert page >= 1
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        for op, attr, val in queries:
            builder.where(op, attr, val)
        builder.order(sort_key, direction)
        builder.skip((page - 1) * page_size)
        builder.limit(page_size)

        result = await builder.read()
        return result.get()
