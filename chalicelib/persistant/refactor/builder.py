import logging
from collections import OrderedDict
from typing import Any, Dict, Literal

from chalice import NotFoundError
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ASCENDING, DESCENDING

from chalicelib.entity.util import ENTITY_MAP
from chalicelib.persistant.refactor.sqs.command import AsyncSqsAddModifyEqualCommand
from chalicelib.persistant.refactor.sqs.model.message import Data, Filter
from chalicelib.service_refactor.interface.builder import BuilderIfs
from chalicelib.service_refactor.model.enum import OperatorEnum
from chalicelib.service_refactor.model.result import Result


class AsyncMongoBuilder(BuilderIfs):
    """
    read, update 연산이 Async로 동작한다.
    """

    def __init__(self, db_name: str, rel_name: str, rel: AsyncIOMotorCollection):
        self.__db_name = db_name
        self.__rel_name = rel_name
        self.__entity = ENTITY_MAP[db_name][rel_name]
        self.__coll = rel
        self.__proj = {}
        self.__filter: Dict[str, Dict[str, Any]] = OrderedDict()
        self.__order = OrderedDict()
        self.__limit = None
        self.__skip = None
        # Default: AND 로 Filter를 적용한다.
        self.__and = False
        self.__or = False
        self.logger = logging.getLogger(__name__)

    def project(self, attr: str) -> "BuilderIfs":
        """
        :param attr: 반환할 속성
        """
        self.__proj[attr] = True
        return self

    def where(self, op: OperatorEnum, attr: str, val: Any) -> "BuilderIfs":
        match op:
            case OperatorEnum.NOT_EQUAL:
                self.__filter[attr] = {"$ne": val}
            case OperatorEnum.EQUAL:
                self.__filter[attr] = {"$eq": val}
            case OperatorEnum.GREATER_THAN:
                self.__filter[attr] = {"$gt": val}
            case OperatorEnum.LESS_THAN:
                self.__filter[attr] = {"$lt": val}
            case OperatorEnum.GREATER_OR_EQUAL_THAN:
                self.__filter[attr] = {"$gte": val}
            case OperatorEnum.LESS_OR_EQUAL_THAN:
                self.__filter[attr] = {"$lte": val}
            case OperatorEnum.IN:
                assert isinstance(val, list)
                if None in val:
                    self.__filter[attr] = {"$in": val}
                else:
                    self.__filter[attr] = {"$exists": True, "$in": val}
            case OperatorEnum.NOT_IN:
                assert isinstance(val, list)
                if None in val:
                    self.__filter[attr] = {"$nin": val}
                else:
                    self.__filter[attr] = {"$exists": True, "$nin": val}
            case _:
                raise RuntimeWarning(f"{op}는 지원하지 않습니다.")
        return self

    def and_(self) -> "BuilderIfs":
        """
        filters를 AND 연산으로 구할 것인지 판단.
        and/or 중 하나만 가능하다.
        """
        if self.__or is True:
            raise RuntimeError("이미 OR 필터가 설정되었습니다.")
        self.__and = True
        return self

    def or_(self) -> "BuilderIfs":
        """
        filters를 AND 연산으로 구할 것인지 판단.
        and/or 중 하나만 가능하다.
        """
        if self.__and is True:
            raise RuntimeError("이미 AND 필터가 설정되었습니다.")
        self.__or = True
        return self

    def limit(self, n: int) -> "BuilderIfs":
        self.__limit = n
        return self

    def skip(self, n: int) -> "BuilderIfs":
        self.__skip = n
        return self

    def order(self, attr: str, direction: Literal["asc", "desc"]) -> "BuilderIfs":
        if direction == "asc":
            self.__order[attr] = ASCENDING
        elif direction == "desc":
            self.__order[attr] = DESCENDING
        else:
            raise RuntimeError(f"{direction} 지원하지 않는 값입니다.")
        return self

    async def read(self) -> Result:
        # 1. filter 생성
        if not self.__filter:
            filter_ = {}
        elif self.__or:
            filter_ = {"$or": [{k: v} for k, v in self.__filter.items()]}
        else:
            filter_ = {"$and": [{k: v} for k, v in self.__filter.items()]}
        # 2. projection 생성
        projection_ = self.__proj
        # 3. skip & limit 생성
        skip = self.__skip or 0
        limit = self.__limit or 0
        # 4. order 생성
        order_ = [(k, v) for k, v in self.__order.items()]
        if not order_:
            order_ = [("_id", ASCENDING)]

        self.logger.debug(
            f"collection: {self.__coll} filter: {filter_}, projection: {projection_}, "
            f"skip: {skip}, limit: {limit}, order: {order_}"
        )
        # 4. DB Access
        data = (
            await self.__coll.find(filter=filter_, projection=projection_)
            .skip(skip)
            .limit(limit)
            .sort(order_)
            .to_list(None)
        )
        # 5. Result로 래핑
        entities = [self.__entity.from_dict(r) for r in data]
        if len(entities) > 1:
            result = Result(data=entities)
        elif len(entities) == 1:
            result = Result(data=entities[0])
        else:
            raise NotFoundError("데이터를 찾지 못했습니다.")
        return result

    async def update(self, **attrs) -> Result:
        """
        db_update queue로 데이터를 전송한다.
        AND 연산만 허용된다.
        eq 연산만 허용된다.
        """
        # 1. filter 생성
        if self.__or:
            raise RuntimeError("Update 시에는 and 연산만 허용됩니다.")
        filters = []
        for k, v in self.__filter.items():
            for op, val in v.items():
                if op != "$eq":
                    raise RuntimeError("Update 시에는 equal 연산만 허용됩니다.")
                filter_ = Filter(column=k, value=val, op="eq")
                filters.append(filter_)
        # 2. updated 생성
        updated = [Data(column=k, value=v) for k, v in attrs.items()]

        # 3. 실행
        command = AsyncSqsAddModifyEqualCommand(
            rel_name=self.__rel_name,
            db_name=self.__db_name,
            filters=filters,
            updated=updated,
        )
        await command.execute()
        # 4. Filter에 맞는 Entity 반환
        return await self.read()

    async def random(self, n: int) -> Result:
        if not self.__filter:
            filter_ = {}
        elif self.__or:
            filter_ = {"$or": [{k: v} for k, v in self.__filter.items()]}
        else:
            filter_ = {"$and": [{k: v} for k, v in self.__filter.items()]}
        self.logger.debug(f"collection: {self.__coll} filter: {filter_} n: {n}")
        pipeline = [{"$match": filter_}, {"$sample": {"size": n}}]
        data = await self.__coll.aggregate(pipeline).to_list(None)
        entities = [self.__entity.from_dict(r) for r in data]
        if len(entities) > 1:
            result = Result(data=entities)
        elif len(entities) == 1:
            result = Result(data=entities[0])
        else:
            raise NotFoundError("데이터를 찾지 못했습니다.")
        return result

    async def count(self) -> int:
        if not self.__filter:
            filter_ = {}
        elif self.__or:
            filter_ = {"$or": [{k: v} for k, v in self.__filter.items()]}
        else:
            filter_ = {"$and": [{k: v} for k, v in self.__filter.items()]}
        result = await self.__coll.count_documents(filter=filter_)
        return result
